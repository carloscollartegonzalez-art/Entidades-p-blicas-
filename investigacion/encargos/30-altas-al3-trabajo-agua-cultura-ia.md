# Altas AL3: trabajo, agua, cultura e IA

Encargo literal enviado a un agente de investigación (Claude, tipo `general-purpose`), con las rutas adaptadas a esta carpeta.

---

Eres un investigador de organización administrativa y presupuestos públicos españoles. Lee primero investigacion/BRIEF_ALTAS.md (criterios de inclusión, método obligatorio, formato de salida), luego investigacion/headers.json y investigacion/ejemplos_altas.json.

Tu lote: investigacion/lotes/AL3.json (7 candidatos: Observatorio Estatal de la Incapacidad Temporal; Observatorio Estatal de Condiciones de Trabajo; Observatorio Nacional de Sequías e Inundaciones; Observatorio de Museos de España; Observatorio Estatal de los Servicios Deportivos a las AAPP; Observatorio del Impacto Social de los Algoritmos (OBISAL); Observatorio de la gestión del agua en España).

Para cada uno: decide si entra (las tres condiciones del brief: sector público estatal, creado o transformado desde 17/04/2004, acto oficial que lo crea o aprueba) y, si entra, rellena la ficha completa con fuentes oficiales. Prioriza encontrar la norma de creación (BOE) y lo que dice sobre gasto, medios y retribución de miembros. Para el de Incapacidad Temporal, comprueba si la orden ministerial ya se ha publicado (posible resolución en BOE de 28/05/2026). Para el de gestión del agua, si es solo una herramienta, exclúyelo pero anota en "motivo" el importe del contrato si aparece en una fuente oficial. Máximo unas 30 búsquedas web en total.

Escribe el resultado en datos/resultados/AL3.json y valida que es JSON correcto. Respuesta final: resumen breve (máx. 12 líneas).
