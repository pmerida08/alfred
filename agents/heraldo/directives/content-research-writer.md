# Directiva: content-research-writer — Escribe con research y citas

## Objetivo

Producir contenido apoyado en investigación real y verificable: posts, hilos o artículos que afirman datos, cifras o tendencias con sus fuentes citadas. Cero invención.

## Trigger

Pablo pide contenido "con datos", "con fuentes", basado en un informe/estudio, o sobre un tema que exige rigor (tendencias, cifras de mercado, comparativas técnicas).

## Reutiliza

Skills de Alfred **`quick-research`** (o **`deep-research`** si es a fondo) para la fase de investigación, y **`article-writing`** para la redacción larga. HERALDO orquesta ambas.

## Inputs

- Tema y ángulo.
- Perfil y plataforma (condiciona longitud y formato).
- Nivel de profundidad (rápido vs. a fondo).

## Proceso

1. **Investigar** con `quick-research`/`deep-research`: reunir hechos, cifras y fuentes primarias. Guardar cada afirmación con su URL de origen.
2. **Verificar:** descartar datos sin fuente sólida. No usar cifras que no se puedan enlazar.
3. **Escribir** con la voz del perfil: integrar los datos como argumento, no como adorno. El research sostiene la tesis, no la sustituye.
4. **Citar:** enlaces o menciones de fuente al pie (o en respuesta, en X). Distinguir dato de opinión.
5. Pasar por `humanise-text` (que el rigor no lo vuelva acartonado).
6. Registrar en Notion con las fuentes en `Notas`.

## Salida

- Pieza redactada con datos integrados + bloque de fuentes citadas.
- Registro en Notion (fuentes en `Notas`).

## Edge cases

- **Fuente dudosa o secundaria:** buscar la primaria; si no existe, no afirmar el dato.
- **Datos contradictorios entre fuentes:** exponer el rango o el conflicto, no elegir el que conviene.
- **Tema sin research disponible:** decírselo a Pablo; no rellenar con cifras inventadas.
