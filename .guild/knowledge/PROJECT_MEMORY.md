# Project Memory

## Product

- Guild is a portable, provider-neutral Agentic SDLC framework.
- It coordinates software work through profiles, skills, workflows, artifacts, gates and policies.
- It must work in conversations, repositories and different agent clients.

## Architecture

- `.guild/` is the canonical provider-neutral source.
- The first implementation is declarative.
- Codex and Claude files are adapters generated from canonical definitions.
- QA and security remain independent from implementation.

## Current constraints

- Do not build a SaaS platform yet.
- Do not require a specific programming language.
- Do not grant production access automatically.
