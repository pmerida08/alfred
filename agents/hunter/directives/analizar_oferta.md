# Directiva: analizar una oferta

**Objetivo:** decir a Pablo si le merece la pena presentarse a una oferta y qué destacar, con un fit score justificado.

**Inputs:** la oferta (texto o URL) y el CV base.

## Pasos

1. **Duplicados:** comprueba Notion según `agents/hunter/CLAUDE.md`. Si ya está enviada, dilo en una línea («Ya enviaste a [Empresa] para [Puesto] el [fecha]») y para.
2. **Lee la oferta y el CV.** Si la URL no se deja leer (Indeed suele devolver 401 a WebFetch y al MCP), ábrela en el Browser pane.
3. **Separa lo que pide:** requisitos obligatorios, deseables, experiencia (años y tipo), soft skills explícitas y contexto de la empresa. Marca cada requisito como cumple, cumple a medias o no cumple.
4. **Fit score de 1 a 10**, redondeado: stack técnico 40 % (obligatorios cubiertos), experiencia 35 %, soft skills explícitas 25 %. Si la oferta no trae requisitos técnicos claros, puntúa por experiencia y contexto.

## Salida

```
## [Empresa] — [Puesto]
**Fit score: X/10** · [modalidad y ubicación]

### Puntos fuertes
### Gaps
### Qué destacar en la candidatura
### Recomendación
[una frase: si presentarse y por qué]
```

El análisis va en español aunque la oferta esté en inglés. Con un fit menor de 4, dilo claramente y no prepares materiales salvo que Pablo lo pida. Si la oferta es demasiado genérica para puntuarla, dilo y pide más contexto.
