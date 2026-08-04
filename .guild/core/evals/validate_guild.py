#!/usr/bin/env python3
"""Lightweight structural validator for the Guild canonical repository.

Checks, over every YAML/JSON file under .guild/ (both core/ and state/):
  1. Syntax   - the file parses as valid YAML/JSON.
  2. Schemas  - every *.schema.json file under .guild/core/schemas/ is
                itself a valid JSON Schema (draft 2020-12).
  3. Instances- every non-schema file that declares a top-level `schema:`
                id is validated against the matching schema, including
                cross-schema $ref (e.g. workflow -> workflow-step).
  4. IDs      - every value found under a key literally named `id` must be
                unique across the whole canonical tree.
  5. Refs     - every value listed under a key named `depends_on` must
                resolve to a known id.

Usage:
    python3 .guild/core/evals/validate_guild.py
Exit code is 0 when there are no errors, 1 otherwise.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, RefResolver
from jsonschema.exceptions import SchemaError

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/ (parent of core/ and state/)
CORE_ROOT = GUILD_ROOT / "core"
SCHEMAS_DIR = CORE_ROOT / "schemas"
TEMPLATES_DIR = CORE_ROOT / "templates"


def _stringify_dates(obj):
    """YAML auto-parses unquoted ISO dates into date/datetime objects.
    Normalize them back to strings so schema `format: date` checks apply."""
    if isinstance(obj, dict):
        return {k: _stringify_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_stringify_dates(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj


def _load(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _iter_guild_files():
    for path in sorted(GUILD_ROOT.rglob("*")):
        if path.suffix in (".yaml", ".yml", ".json"):
            yield path


def _collect_ids_and_refs(data, source: str, ids: dict, refs: list):
    """Recursively collect `id:` values and `depends_on:` reference lists."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "id" and isinstance(value, str):
                ids.setdefault(value, []).append(source)
            if key == "depends_on" and isinstance(value, list):
                for ref in value:
                    if isinstance(ref, str):
                        refs.append((ref, source))
            _collect_ids_and_refs(value, source, ids, refs)
    elif isinstance(data, list):
        for item in data:
            _collect_ids_and_refs(item, source, ids, refs)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    schema_files = sorted(SCHEMAS_DIR.glob("*.schema.json"))
    schema_store: dict[str, dict] = {}       # $id (URI)          -> schema, for $ref resolution
    schema_by_guild_id: dict[str, dict] = {} # guildSchemaId      -> schema, for instance lookup
    parsed_files: dict[Path, object] = {}

    # Pass 1: parse every file.
    for path in _iter_guild_files():
        rel = path.relative_to(GUILD_ROOT.parent)
        try:
            parsed_files[path] = _load(path)
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            errors.append(f"[parse] {rel}: {exc}")

    # Pass 2: validate schema files and build the $id -> schema store.
    for path in schema_files:
        rel = path.relative_to(GUILD_ROOT.parent)
        schema = parsed_files.get(path)
        if schema is None:
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"[schema-invalid] {rel}: {exc.message}")
            continue
        schema_id = schema.get("$id")
        guild_id = schema.get("guildSchemaId")
        if not schema_id or not guild_id:
            errors.append(f"[schema-missing-id] {rel}: schema needs both $id and guildSchemaId")
            continue
        if schema_id in schema_store:
            errors.append(
                f"[schema-duplicate-id] {rel}: $id '{schema_id}' already used by "
                f"another schema file"
            )
            continue
        if guild_id in schema_by_guild_id:
            errors.append(
                f"[schema-duplicate-id] {rel}: guildSchemaId '{guild_id}' already used by "
                f"another schema file"
            )
            continue
        schema_store[schema_id] = schema
        schema_by_guild_id[guild_id] = schema

    # Pass 3: validate instances against their declared schema.
    # Templates are illustrative placeholders (e.g. id: replace-with-...),
    # not real instances, so they are exempt from schema and reference checks.
    for path, data in parsed_files.items():
        if path in schema_files or path.parent == SCHEMAS_DIR:
            continue
        if TEMPLATES_DIR in path.parents:
            continue
        if not isinstance(data, dict) or "schema" not in data:
            continue
        rel = path.relative_to(GUILD_ROOT.parent)
        schema_id = data["schema"]
        schema = schema_by_guild_id.get(schema_id)
        if schema is None:
            errors.append(
                f"[schema-not-found] {rel}: declares schema '{schema_id}' which "
                f"has no matching file under .guild/core/schemas/"
            )
            continue
        resolver = RefResolver(base_uri="", referrer=schema, store=schema_store)
        validator = Draft202012Validator(schema, resolver=resolver)
        instance = _stringify_dates(data)
        for validation_error in validator.iter_errors(instance):
            loc = "/".join(str(p) for p in validation_error.absolute_path) or "<root>"
            errors.append(f"[instance-invalid] {rel} ({loc}): {validation_error.message}")

    # Pass 4 + 5: collect ids and depends_on references, excluding schema files.
    ids: dict[str, list[str]] = {}
    refs: list[tuple[str, str]] = []
    for path, data in parsed_files.items():
        if path in schema_files or path.parent == SCHEMAS_DIR:
            continue
        if TEMPLATES_DIR in path.parents:
            continue
        rel = str(path.relative_to(GUILD_ROOT.parent))
        _collect_ids_and_refs(data, rel, ids, refs)

    for id_value, sources in ids.items():
        if len(sources) > 1:
            errors.append(
                f"[duplicate-id] '{id_value}' used in multiple places: "
                f"{', '.join(sources)}"
            )

    for ref, source in refs:
        if ref not in ids:
            warnings.append(
                f"[unresolved-ref] {source}: depends_on references unknown id '{ref}'"
            )

    # Report.
    files_scanned = len(parsed_files)
    print(f"Guild validation: {files_scanned} file(s) scanned, "
          f"{len(schema_by_guild_id)} schema(s) loaded.")
    for warning in warnings:
        print(f"WARNING {warning}")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"\nOK ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
