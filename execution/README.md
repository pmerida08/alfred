# Execution — Scripts Python del sistema Alfred

## ¿Qué va aquí?

Scripts Python deterministas que implementan **el cómo** de cada proceso.

Cada script hace una cosa bien definida. Alfred los encadena según la directiva correspondiente.

## Reglas

- **Credenciales:** siempre desde `.env`, nunca en el código.
- **Sin lógica de negocio:** la lógica está en la directiva, no en el script.
- **Idempotentes cuando sea posible:** ejecutar dos veces no debe romper nada.
- **Archivos temporales:** usar `.tmp/` para intermedios.
- **Antes de crear uno nuevo:** verificar que no existe ya un script equivalente.

## Estructura recomendada de un script

```python
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # lógica aquí
    pass

if __name__ == "__main__":
    main()
```

## Convenciones de nombres

`<dominio>_<accion>.py` — ejemplos:
- `email_fetch.py`
- `calendar_list_events.py`
- `notion_push_tasks.py`
