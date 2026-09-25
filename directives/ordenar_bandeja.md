# Directiva: Ordenar la bandeja de entrada

**Dominio:** Email
**Cuándo:** En la primera sesión del día en el PC de Pablo (hook `.claude/hooks/bandeja_diaria.sh`) o cuando Pablo lo pida
**Autonomía:** Etiquetar y archivar sin preguntar. **Nunca borrar, nunca enviar, nunca marcar como spam.**

---

## Objetivo

Que en la bandeja de entrada solo queden las respuestas reales, los procesos de selección abiertos y lo urgente. El resto se etiqueta y se archiva (sigue en su etiqueta y en "Todos"; es reversible).

## Etiquetas

| Etiqueta | Qué va | ¿Sale de la bandeja? |
|---|---|---|
| `Empleo/Respuestas` | Correos escritos por una persona o con novedades de un proceso: entrevistas, pruebas técnicas, peticiones de CV, rechazos | No |
| `Empleo/Candidaturas` | Acuses automáticos de candidatura (join.com, Mercadona RRHH, NTT DATA, Izertis, Adecco, Teamtailor, Greenhouse…) | No |
| `Empleo/Alertas` | LinkedIn (jobalerts, jobs-noreply), Indeed, Tecnoempleo alertas, Handshake, Experteer, best-jobs-online, jobs2web, InfoJobs | Sí, si tiene más de 2 días |
| `Finanzas` | Bcas, Stripe, bancos, facturas, compras (Alsa, Amazon pedidos) | No |
| `Newsletters` | Supabase, Pletor, Voiceflow, IdeaBrowser, TopCV, LinkedIn newsletters, Upwork, publicidad (Amazon ofertas, El Corte Inglés, Airbnb, Spotify, Certideal) | Sí |

Los IDs de etiqueta se obtienen con `list_labels`. Si alguna no existe, crearla con `create_label`.

## Pasos

1. `search_threads` con `in:inbox has:nouserlabels newer_than:7d` (pageSize 50, paginar). Solo toca lo que aún no tiene etiqueta, así cada arranque es rápido e idempotente.
   - Primera ejecución: usar `newer_than:30d` en lugar de `7d`.
2. Clasificar cada hilo por remitente y asunto según la tabla. Ante la duda entre `Respuestas` y otra categoría → `Respuestas` (mejor que sobre a que se pierda).
3. `label_thread` con la etiqueta. Si toca archivar, `unlabel_thread` con `INBOX`.
4. Lo que no encaje en ninguna categoría: dejarlo en la bandeja sin etiquetar.
5. Informar a Pablo en **una o dos líneas**, y solo destacar lo que requiere acción:
   ```
   Bandeja ordenada: 23 hilos (4 archivados como alertas, 6 newsletters). Nuevo en Empleo/Respuestas: [Remitente] — [asunto].
   ```
   Si no había nada que ordenar: `Bandeja al día.`
6. Después, atender lo que Pablo haya pedido en su primer mensaje.

## Edge cases

- **El conector de Gmail no tiene permiso de escritura** (`This connector requires additional permissions`): avisar a Pablo una vez con "El conector de Gmail solo tiene lectura; reconéctalo en Configuración → Conectores para poder ordenar la bandeja" y seguir con la sesión. No reintentar.
- **Sesiones desde Telegram / servidor Linux**: el hook está en git, pero solo inyecta la orden en Windows (comprueba `uname`). Si llega aquí por otra vía, no ejecutar salvo que Pablo lo pida.
- **Un correo de Bcas u otro aviso de cobro**: nunca archivar; mencionarlo en el resumen si sigue sin leer.
- **Correos de personas conocidas** (familia, profesores, contactos de ADA, Manu): no archivar nunca.
- No marcar como leído: Pablo decide qué ha leído.
