# Guild Bootstrap Pack

Este paquete sirve para iniciar **Guild**, un framework portable y agnóstico de proveedor para coordinar agentes IA durante el ciclo de vida del software.

## Qué hacer

1. Copia el contenido en un repositorio Git nuevo.
2. Abre el repositorio con Codex o Claude Code.
3. Ejecuta los prompts de `bootstrap-prompts/` en orden.
4. Revisa y confirma cada fase antes de pasar a la siguiente.

## Orden de ejecución

1. `bootstrap-prompts/01-foundation.md`
2. `bootstrap-prompts/02-agents.md`
3. `bootstrap-prompts/03-workflows.md`
4. `bootstrap-prompts/04-adapters-and-validation.md`

La fuente canónica inicial está en `.guild/core/spec/GUILD_MASTER_SPEC.md`.

No construyas todavía una plataforma SaaS, una interfaz gráfica ni un runtime multiagente. La primera versión debe ser declarativa y portable.
