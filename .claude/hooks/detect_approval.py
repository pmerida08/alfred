import sys
import json
import re

try:
    data = json.load(sys.stdin)
    msg = ""
    if isinstance(data, dict):
        msg = data.get("message", "") or data.get("user_message", "") or str(data)
    else:
        msg = str(data)
except Exception:
    msg = sys.stdin.read()

msg_lower = msg.lower().strip()

APPROVAL_PATTERNS = [
    r"\bperfecto\b", r"\bgenial\b", r"\bexcelente\b", r"\bestupendo\b",
    r"\bfenomenal\b", r"\bguay\b", r"\bbrutala?\b", r"\bmola\b",
    r"\bchulo\b", r"\bok\b", r"\bbuenísimo\b", r"\bbuenisimo\b",
    r"\bmuy bien\b", r"\bbien hecho\b", r"\bjusto lo que\b",
    r"\beso es\b", r"\basí\b.*\bquería\b", r"\bquería eso\b",
    r"\bgracias.*queda(do)?\b", r"\bqueda (bien|genial|perfecto)\b",
    r"\blisto\b", r"\badelante\b", r"\bprocede\b",
]

is_approval = any(re.search(p, msg_lower) for p in APPROVAL_PATTERNS)

if is_approval:
    print(
        "RECORDATORIO ALFRED: El usuario acaba de expresar satisfacción o aprobación. "
        "Si en esta sesión acabas de completar o implementar una funcionalidad nueva, "
        "pregúntale: '¿Subo los cambios a GitHub?'. "
        "Solo pregunta si hay cambios reales que subir — no preguntes en conversaciones informativas."
    )
