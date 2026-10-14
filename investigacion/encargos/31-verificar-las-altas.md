# Verificación independiente de las 10 altas

Encargo literal enviado a un agente de investigación (Claude, tipo `general-purpose`), con las rutas adaptadas a esta carpeta.

---

Eres un verificador independiente: no has participado en la investigación. Lee datos/resultados/AL1.json, AL2.json y AL3.json. Para cada entrada con "incluir": true (10 en total), comprueba contra la fuente oficial primaria (BOE, boletines oficiales, La Moncloa, webs de ministerios u organismos, Diario de Sesiones):

1. La norma o acto de creación o transformación que figura en «Norma fundacional» y su fecha («Fecha legal»): ¿existe, dice lo que se afirma y la fecha es correcta?
2. El «Periodo presidencial» (Zapatero 17/04/2004–20/12/2011, Rajoy 21/12/2011–01/06/2018, Sánchez desde 02/06/2018) según esa fecha.
3. La afirmación de «Estado de cuantificación» / «Presupuesto: texto completo» sobre gasto (p. ej. «no supondrá incremento del gasto», miembros sin retribución): ¿lo dice la norma, en qué artículo o apartado?
4. El «Estado legal y operativo» (creado, constituido, en tramitación, no constituido).

Reglas: WebFetch solo funciona con URLs que hayan salido en resultados de WebSearch (busca primero). Si una URL del BOE con «?id=» devuelve otro título, descártala; prefiere URL ELI (boe.es/eli/...). Máximo unas 35 búsquedas web. No modifiques los ficheros de resultados.

Escribe datos/resultados/verificacion_altas.json: lista con un objeto por entidad {"candidato", "norma_ok": "COINCIDE|DISCREPA|NO VERIFICABLE", "fecha_ok": ..., "periodo_ok": ..., "gasto_ok": ..., "estado_ok": ..., "correcciones": "qué habría que cambiar, con cita literal y URL", "fuentes": [...]}. Valida el JSON. Respuesta final: tabla breve entidad → resultado y las correcciones necesarias (máx. 15 líneas).
