# 2. Investigación

La búsqueda de cifras la hicieron agentes de investigación: instancias de Claude con búsqueda web, cada una con un encargo y un lote de entidades. Todo lo que recibieron y todo lo que devolvieron está en esta carpeta, así que cualquiera puede revisar de dónde sale cada número o repetir la búsqueda con otro agente o a mano.

## Piezas

- **Instrucciones comunes:**
  - [`investigacion/BRIEF.md`](../investigacion/BRIEF.md): presupuesto y personal. Recoge las reglas del método, las columnas, el vocabulario, el acceso web y el formato de salida.
  - [`investigacion/BRIEF_PERSONAL.md`](../investigacion/BRIEF_PERSONAL.md): desglose del personal por tipo de puesto.
  - [`investigacion/BRIEF_DUP.md`](../investigacion/BRIEF_DUP.md): mapa de duplicidades entre el Estado y las comunidades.
- **Contexto:** [`headers.json`](../investigacion/headers.json) (las 73 cabeceras exactas de la hoja) y [`ejemplos.json`](../investigacion/ejemplos.json) (tres filas bien rellenas que sirven de modelo).
- **Lotes:** [`investigacion/lotes/`](../investigacion/lotes/). Cada uno recoge las filas que recibió un encargo, con los campos que ya estaban rellenos.
- **Encargos:** [`investigacion/encargos/`](../investigacion/encargos/). Es el texto literal de los 27 encargos.
- **Resultados:** [`datos/resultados/`](../datos/resultados/). Hay un JSON por encargo.
- **Código de los agentes:** [`investigacion/scripts-agentes/`](../investigacion/scripts-agentes/). Son los scripts con los que 17 de los 27 encargos generaron su JSON; al ejecutarlos se obtiene exactamente el resultado guardado. Las notas de trabajo están en [`investigacion/notas/`](../investigacion/notas/).

## Rondas

| Ronda | Encargos | Qué buscaba | Resultado |
|---|---|---|---|
| 1. Presupuesto y personal | 01–08 (lotes A–G) | Presupuesto propio, capítulo 1 (crédito, obligaciones y pagos) y plantilla de las 125 fichas, por bloques: entes estatales, órganos colegiados estatales, plantillas estatales y comunidades agrupadas | `A_…` a `G_…` |
| 2. Huecos | 09–13 (R2A–R2E) | Lo que quedó vacío en la ronda 1, con pistas de lo que no funcionó | `R2A_…` a `R2E_…` |
| Verificación | 14 | Un revisor independiente coteja con la fuente 20 cifras nuevas elegidas al azar (`investigacion/verificar.json`) | `verificacion.json`: 20/20 coinciden |
| Desglose de personal | 15–20 (P1–P6) | Núcleo y administración, libre designación, altos cargos y eventuales de las entidades con presupuesto | `P1_…` a `P6_…` |
| Duplicidades | 21–25 (D1–D5) | 21 temas × Estado y 17 comunidades | `DUP1.json` a `DUP5.json` |
| Coste de los órganos sin presupuesto | 26 | Qué dice cada norma sobre medios, secretaría y dietas de los 40 órganos consultivos | `C_apoyo.json` |
| CNMC y CSIC | 27 | En qué se gasta el presupuesto: capítulos y destino | `gasto_csic_cnmc.json` |

## Formato de cada resultado

```json
[{"ID": 23,
  "updates": {"<cabecera exacta de la hoja>": "<valor>"},
  "fuentes_nuevas": ["https://…"],
  "verificacion": "documento, página/tabla/fila, unidad original y conversión",
  "no_encontrado": "qué se buscó y no apareció"}]
```

`scripts/apply.py` aplica los resultados en el orden indicado: si dos encargos tocan la misma celda, gana el último. Los campos `verificacion` y `no_encontrado` acaban en la hoja «Verificación y pendientes».

## Problemas encontrados y cómo se resolvieron

- **El agente solo puede leer páginas que hayan salido en una búsqueda.** Si pide una URL directa, la herramienta la rechaza. Por eso los encargos dicen que hay que buscar primero el documento.
- **Los PDF largos (leyes de presupuestos, informes de la IGAE) se cortan.** Hay que leerlos por tramos y pedir la cita literal de la fila, no un resumen. En la IGAE, el gasto por capítulos está en miles de euros.
- **Las URL del BOE con «?id=» devolvían a veces otro documento** cuando varios agentes trabajaban a la vez. Hay que comprobar siempre que el título coincide; el verificador detectó un caso (ID 96).
- **Hay un cupo de búsquedas compartido entre agentes simultáneos.** Se repartió en unas 30 búsquedas por agente.
- **Algún agente escribió en columnas que no debía tocar.** `apply.py` protege ID, «URL del documento», «Fecha de revisión» y «Fuentes de la ficha»: las URL nuevas se añaden a «Fuentes de la ficha» sin borrar las anteriores.

## Repetir o ampliar

1. Copia el encargo que corresponda de `investigacion/encargos/` y cambia el lote. Para una entidad nueva, añádela antes a la hoja de `datos/entrada/` con un ID nuevo.
2. Dáselo a un agente con búsqueda web, o síguelo a mano. Las reglas valen igual para una persona.
3. Guarda el JSON en `datos/resultados/` y añádelo a la lista `ORDEN` de `scripts/apply.py`, antes de `Z_clasificacion.json`.
4. Ejecuta `python scripts/run_all.py` y revisa en la hoja «Cambios» qué ha cambiado.
5. Antes de dar por buena una tanda, pide a otro agente o a otra persona que coteje una muestra con la fuente, como en el encargo 14.

Para actualizar a otro año o corte, por ejemplo la ejecución a 31/12/2026:
- cambia `REV_DATE` y el literal `CUT` en `apply.py`;
- cambia las fechas de corte en `BRIEF.md`.
