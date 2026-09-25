# Skill: deploy-alfred — subir cambios de Alfred a GitHub

**Cuándo:** Pablo pide subir los cambios de Alfred, abrir el PR o fusionarlo.

Solo existen las ramas `alfred` y `main`: se trabaja en `alfred` y se llega a `main` por PR. Nunca se crean ramas temporales y nunca se borra `alfred` al fusionar (sin `--delete-branch`).

1. `git status` y `git diff --stat`: si no hay cambios, dilo y para. Commit de lo pendiente con mensaje semántico (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`).
2. Si el cambio añade un agente o una capacidad visible, actualiza `dashboard.html` (array `BRANCHES` y los contadores del pie).
3. `git push origin alfred` y `gh pr create --base main --head alfred` con un resumen de qué cambia y cómo se probó.
4. Para fusionar: comprueba `gh pr view <n> --json mergeable,mergeStateStatus` y `gh pr merge <n> --merge`. El hook de PostToolUse trae `main` a la copia local; después, `git push origin alfred` para que las dos ramas queden iguales.
5. Si el push o el merge fallan por conflictos, informa sin forzar.

La web https://alfred-pa.netlify.app no se actualiza con el merge: se despliega a mano desde `.tmp/netlify-deploy/`.
