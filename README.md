# Guild

**Guild** es un framework portable y agnóstico de proveedor para coordinar agentes de IA
durante todo el ciclo de vida del software. Define catorce perfiles —cada uno con un alias
de D&D: DM, Paladin, Fighter, Druid, Bard, Ranger, Artificer, Wizard, Warlock, Barbarian,
Rogue, Cleric, Sorcerer y Monk—, las skills que usan, los workflows que siguen (onboarding,
nuevo proyecto, nueva funcionalidad, corrección de bugs, mejora de producto y revisión de
PRs), los contratos con que se pasan el trabajo y las aprobaciones humanas que nunca se
saltan. Todo es declarativo (Markdown, YAML y JSON Schema), así que funciona con Claude
Code, con Codex o con cualquier asistente que sepa leer ficheros, y en cualquier lenguaje
o stack.

Este README es el manual para aplicar Guild a un proyecto, tanto si ya existe como si
empieza desde cero, hasta que arranca el onboarding.

---

## Cómo está organizado

Guild vive en tu repositorio bajo `.guild/`, separado en dos partes:

| Directorio | Qué es | Quién lo escribe |
|---|---|---|
| `.guild/core/` | El framework: perfiles, skills, workflows, schemas, políticas, generador de adaptadores y evals | Se copia de este repositorio y se reemplaza entero al actualizar Guild |
| `.guild/state/` | El conocimiento, la planificación y el historial de tu proyecto | Lo crea el onboarding y lo mantienen los perfiles. Una actualización de Guild nunca lo toca |

A partir de `.guild/core/` se generan los ficheros que lee cada cliente:

| Fichero generado | Para |
|---|---|
| `.claude/agents/<perfil>.md` | Subagentes de Claude Code, uno por perfil |
| `.claude/skills/<skill>/SKILL.md` | Skills de Claude Code |
| `.agents/skills/<skill>/SKILL.md` | Skills de Codex |
| `AGENTS.md`, `CLAUDE.md` | Un bloque gestionado con las reglas de Guild |
| `.claude/settings.json` | Una regla de permisos derivada de las políticas: prohíbe el force-push |

## Requisitos

- Un repositorio Git, ya sea uno existente o uno nuevo vacío.
- Python 3 con [PyYAML](https://pypi.org/project/PyYAML/) para el generador de adaptadores.
  Las comprobaciones opcionales usan además [jsonschema](https://pypi.org/project/jsonschema/).

  ```sh
  pip install pyyaml jsonschema
  ```

- Un cliente de agente, como Claude Code o Codex. Cualquier asistente que lea ficheros
  también sirve: recorre los workflows paso a paso, cambiando de perfil (ver
  [`EXECUTION_MODES.md`](.guild/core/workflows/EXECUTION_MODES.md)).

---

## 1. Instalar Guild

Instalar Guild siempre consiste en lo mismo: copiar `.guild/core/` a tu repositorio y
ejecutar el generador allí. **Nunca copies `.guild/state/`**: ese directorio pertenece a
cada proyecto, y el tuyo lo creará el onboarding.

### En un proyecto que ya existe

Desde la raíz de tu repositorio:

```sh
git clone https://github.com/xavitoro/guild.git /tmp/guild
mkdir -p .guild
cp -r /tmp/guild/.guild/core .guild/core
python3 .guild/core/adapters/generate_adapters.py --target .
```

Qué pasa con lo que ya tienes:

- **`AGENTS.md` y `CLAUDE.md` existentes no se sobrescriben.** El generador añade un bloque
  delimitado por `<!-- guild:adapter:start -->` y `<!-- guild:adapter:end -->`, y lo que
  hay fuera de él queda intacto. Al regenerar, solo se actualiza lo que va entre los marcadores.
- **Tus subagentes y skills propios se respetan.** El generador solo toca los ficheros que
  llevan su cabecera `GENERATED FILE — DO NOT EDIT BY HAND`.

### En un proyecto nuevo

Crea primero el repositorio y después instala Guild igual:

```sh
mkdir mi-proyecto && cd mi-proyecto
git init
git clone https://github.com/xavitoro/guild.git /tmp/guild
mkdir -p .guild
cp -r /tmp/guild/.guild/core .guild/core
python3 .guild/core/adapters/generate_adapters.py --target .
```

Como el repositorio no tiene `AGENTS.md` ni `CLAUDE.md`, el generador los crea solo con el
bloque de Guild. Puedes escribir tus propias instrucciones encima o debajo del bloque.

> **Consejo para Claude Code:** si quieres que Claude Code lea también las reglas de
> `AGENTS.md`, que son más detalladas que el resumen de `CLAUDE.md`, añade una línea
> `@AGENTS.md` al principio de `CLAUDE.md`, fuera del bloque generado.

### Comprobar la instalación

```sh
python3 .guild/core/evals/validate_guild.py                            # sintaxis, schemas, ids y referencias
python3 .guild/core/adapters/generate_adapters.py --target . --check   # los adaptadores coinciden con el core
```

Los dos deben terminar en `OK`.

### Hacer commit

Haz commit de `.guild/core/` y de los ficheros generados. Están pensados para versionarse,
no para regenerarse en cada clon:

```sh
git add .guild/core .claude .agents AGENTS.md CLAUDE.md
git commit -m "chore: install Guild"
```

---

## 2. Hacer el onboarding

Con Guild instalado, abre el repositorio con tu cliente de agente y pide el onboarding:

| Tu caso | Pídelo así, por ejemplo | Workflow |
|---|---|---|
| Proyecto que ya tiene código | «Haz el onboarding de este proyecto con Guild» | `onboard-existing-project` |
| Proyecto nuevo | «Crea un proyecto nuevo con Guild: una app para…» | `create-new-project` |

**Si se te olvida:** mientras no exista `.guild/state/project.yaml`, cualquier otra
petición que hagas recibe primero esta pregunta del DM: ¿hacemos antes el onboarding?
- Si dices que sí, se hace el onboarding y después se retoma tu petición.
- Si dices que no, tu petición sigue adelante y la pregunta vuelve la próxima vez.

### Qué te va a preguntar

Lo primero, antes que nada, el DM (workflow-knowledge-orchestrator) te hace estas
preguntas. Todas tienen opciones y siempre admiten una respuesta con tus propias palabras.

1. **Tres idiomas**, por separado:
   - el idioma en que Guild conversa contigo;
   - el idioma de la prosa que escribe en `.guild/state/` (memoria, plan, decisiones,
     `PROJECT_STATUS.md`…);
   - el idioma de git: commits, pull requests y comentarios de revisión.

   Ids, aliases, claves y nombres de fichero nunca se traducen.
2. **Revisión automática de PRs:** si quieres que el Barbarian (QA), el Rogue (seguridad),
   los dos o ninguno revisen cada pull request como job de CI (una GitHub Action en
   GitHub), y con qué cliente de agente. Lo recomendado es ninguno, porque cada ejecución
   tiene coste y necesita un secreto.
3. **El alcance del onboarding:** el repositorio entero o una parte.

Cada respuesta se guarda en `.guild/state/project.yaml`, y ningún perfil vuelve a
preguntarla ni la deduce por su cuenta. Puedes cambiar cualquiera más adelante; el cambio
se aplica desde ese momento.

### Qué pasa después

**En un proyecto existente** (`onboard-existing-project`), nada cambia tu código de producto:

1. El Artificer descubre el stack, la estructura y las convenciones, citando ficheros como evidencia.
2. El Cleric revisa el CI/CD y la infraestructura, si los hay.
3. El Rogue evalúa la postura de seguridad de partida, si hay autenticación, pagos,
   secretos o datos personales.
4. Si elegiste revisión automática de PRs:
   - el Cleric escribe el job de CI;
   - el Rogue lo revisa;
   - tú apruebas su secreto y su coste antes de activarlo. Guardas tú el secreto en el
     host; ningún perfil ve su valor.
5. El DM consolida en `.guild/state/` lo que se ha verificado, siempre con evidencia.

**En un proyecto nuevo** (`create-new-project`), el recorrido es más largo:

1. Visión con el Paladin y requisitos con el Fighter.
2. Si hay interfaz, la experiencia con el Druid y los textos con el Bard.
3. El esqueleto del proyecto con el Artificer.
4. Revisiones especializadas cuando aplican: base de datos (Wizard), integraciones
   (Warlock) y seguridad (Rogue).
5. La verificación del Barbarian.
6. La revisión automática de PRs, si la elegiste.
7. El primer pull request.
8. Si se despliega, siempre con tu aprobación previa.

**En los dos casos**, cada respuesta de un perfil empieza con su alias, por ejemplo
«Barbarian (quality-assurance-engineer) — …», así que siempre sabes quién habla. Además:

- **Las decisiones que el proyecto no puede resolver solo llegan a ti** con opciones, una
  recomendación y lo que pasa si no respondes. Ese valor por defecto nunca se aplica sin
  que lo hayas visto.
- **Las acciones Red-tier se bloquean hasta que las apruebas explícitamente.** Son las
  acciones de alto riesgo: merge a ramas protegidas, despliegues a producción, migraciones
  destructivas, secretos, permisos, pagos, comunicaciones externas y costes.

Al terminar, haz commit de `.guild/state/`: a partir de ahí es la memoria de tu proyecto.

---

## Después del onboarding

Trabaja pidiendo lo que necesites. El DM elige el workflow:

| Workflow | Para |
|---|---|
| `add-feature` | Una funcionalidad nueva, desde los requisitos hasta un despliegue opcional |
| `fix-bug` | Reproducir, diagnosticar, corregir y verificar un bug |
| `improve-product` | Un ciclo de mejora guiado por datos: evidencia, hipótesis, cambio y medición |
| `review-pull-request` | Revisar una PR de forma independiente, con aprobación humana antes del merge |

Dos garantías se mantienen siempre:
- **Quien implementa nunca aprueba su propia QA ni su propia seguridad.** Esas revisiones
  son del Barbarian y del Rogue.
- **Lo que un perfil detecta y no va a hacer no se pierde:** se registra como deuda
  técnica en el plan, con dueño y evidencia.

## Actualizar Guild

Reemplaza `.guild/core/` entero y regenera los adaptadores. `.guild/state/` no se toca:

```sh
git clone https://github.com/xavitoro/guild.git /tmp/guild-new
rm -rf .guild/core
cp -r /tmp/guild-new/.guild/core .guild/core
python3 .guild/core/adapters/generate_adapters.py --target .
```

Si tu proyecto se incorporó con una versión anterior y todavía no tiene en `project.yaml`
los idiomas o la elección de revisión automática de PRs, el DM te los pregunta en la
siguiente ejecución, en lugar de suponerlos.

## Más información

- [`GUILD_MASTER_SPEC.md`](.guild/core/spec/GUILD_MASTER_SPEC.md): la especificación completa.
- [`INSTALL.md`](.guild/core/adapters/INSTALL.md): la instalación en detalle, incluida la
  instalación global en el directorio de usuario.
- [`workflows/`](.guild/core/workflows/README.md): cada workflow, con su diagrama y sus pasos.
- [`EXECUTION_MODES.md`](.guild/core/workflows/EXECUTION_MODES.md): Guild con un solo
  asistente, con subagentes o con un runtime externo.

Para contribuir a Guild en sí, lee [`AGENTS.md`](AGENTS.md): este repositorio es el código
fuente del framework, no un proyecto gestionado con Guild.

## Licencia

[MIT](LICENSE)
