# 2. Investigación

La búsqueda de cifras la hicieron agentes de investigación: instancias de Claude con búsqueda web, cada una con un encargo y un lote de entidades. Todo lo que recibieron y todo lo que devolvieron está en esta carpeta, así que cualquiera puede revisar de dónde sale cada número o repetir la búsqueda con otro agente o a mano.

## Piezas

- **Instrucciones comunes:**
  - [`investigacion/BRIEF.md`](../investigacion/BRIEF.md): presupuesto y personal. Recoge las reglas del método, las columnas, el vocabulario, el acceso web y el formato de salida.
  - [`investigacion/BRIEF_PERSONAL.md`](../investigacion/BRIEF_PERSONAL.md): desglose del personal por tipo de puesto.
  - [`investigacion/BRIEF_DUP.md`](../investigacion/BRIEF_DUP.md): mapa de duplicidades entre el Estado y las comunidades.
  - [`investigacion/BRIEF_ALTAS.md`](../investigacion/BRIEF_ALTAS.md): cuándo entra una entidad nueva y cómo se rellena su ficha completa.
- **Contexto:** [`headers.json`](../investigacion/headers.json) (las 73 cabeceras exactas de la hoja) y [`ejemplos.json`](../investigacion/ejemplos.json) (tres filas bien rellenas que sirven de modelo; [`ejemplos_altas.json`](../investigacion/ejemplos_altas.json) para las altas).
- **Lotes:** [`investigacion/lotes/`](../investigacion/lotes/). Cada uno recoge las filas que recibió un encargo, con los campos que ya estaban rellenos.
- **Encargos:** [`investigacion/encargos/`](../investigacion/encargos/). Es el texto literal de los 31 encargos.
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
| Altas | 28–30 (AL1–AL3) | 21 observatorios estatales candidatos: si entran en el inventario y, si entran, su ficha completa | `AL1.json` a `AL3.json` |
| Verificación de las altas | 31 | Un revisor independiente comprueba norma, fecha, periodo, gasto y estado de las 10 que entran | `verificacion_altas.json` |

## Formato de cada resultado

```json
[{"ID": 23,
  "updates": {"<cabecera exacta de la hoja>": "<valor>"},
  "fuentes_nuevas": ["https://…"],
  "verificacion": "documento, página/tabla/fila, unidad original y conversión",
  "no_encontrado": "qué se buscó y no apareció"}]
```

`scripts/apply.py` aplica los resultados en el orden indicado: si dos encargos tocan la misma celda, gana el último. Los campos `verificacion` y `no_encontrado` acaban en la hoja «Verificación y pendientes».

## Altas del 14/10/2026

El inventario original tenía 125 entidades creadas o transformadas desde el 17/04/2004 (inicio del Gobierno Zapatero). Al cruzarlo con el catálogo de [observatoriospublicos.es](https://observatoriospublicos.es/) aparecieron 51 observatorios de la Administración del Estado que no estaban. Se buscaron los 21 con más visos de ser órganos del Estado creados desde 2004.

**Cuándo entra una entidad** ([`BRIEF_ALTAS.md`](../investigacion/BRIEF_ALTAS.md)): tiene que cumplir las tres condiciones.
1. Es sector público estatal: un órgano o una entidad de la Administración del Estado, de sus organismos o de sus sociedades, o creado por una ley estatal. No entran proyectos de universidades, fundaciones privadas, asociaciones ni redes financiadas por convenio sin norma que las cree.
2. Se creó o se transformó desde el 17/04/2004: creación, recreación, nueva regulación o constitución efectiva.
3. Hay un acto oficial que lo crea o lo aprueba: ley, real decreto, orden, acuerdo del Consejo de Ministros o proyecto de ley aprobado por el Consejo de Ministros. Si solo está anunciado o en tramitación, entra como «creación anunciada o en tramitación, no constituida».

Las series estadísticas, los portales y las herramientas no entran aunque se llamen «observatorio».

**Entran 10** (IDs por fecha del acto):

| ID | Observatorio | Acto | Periodo |
|---|---|---|---|
| 126 | Nacional de Seguridad Vial (DGT) | RD 1599/2004, art. 10.3 | Zapatero |
| 127 | Militar para la Igualdad entre Mujeres y Hombres en las FAS | Acuerdo del Consejo de Ministros de 04/03/2005 (Orden DEF/524/2005); Orden DEF/111/2019 | Zapatero |
| 128 | Permanente del Mercado de los Servicios Portuarios | Constitución efectiva el 29/06/2012; la ley que lo creó (Ley 48/2003) es anterior al corte | Rajoy |
| 129 | De Igualdad de RTVE | Febrero de 2018, según el Diario de Sesiones; el acuerdo de creación no está publicado | Rajoy |
| 130 | De Salud de las Mujeres | Acuerdo del Consejo de Ministros de 01/03/2019 (Orden PCI/462/2019) | Sánchez |
| 131 | De Buenas Prácticas Regulatorias | Ley 18/2022 (DA 9.ª de la Ley 20/2013) | Sánchez |
| 132 | De Salud y Cambio Climático | Acuerdo del Consejo de Ministros de 18/07/2023 | Sánchez |
| 133 | De la Vivienda Turística | Anunciado por el Gobierno el 21/10/2025; no constituido | Sánchez |
| 134 | Estatal de la Incapacidad Temporal | Anunciado el 09/02/2026; orden no publicada | Sánchez |
| 135 | Para la Prevención del Tabaquismo | Proyecto de ley aprobado por el Consejo de Ministros el 21/07/2026 | Sánchez |

**No entran 11:** OBERAXE (base legal de 2000), Observatorio Estatal de la Dependencia (privado), Precios de los Alimentos (RD 509/2000, ya sustituido por el Observatorio de la Cadena Alimentaria, ID 29), Formación y Social del Transporte por Carretera (web e informes, sin órgano), Condiciones de Trabajo del INSST (portal), Sequías e Inundaciones (no existe como órgano), Museos de España (proyecto de 2018), Servicios Deportivos (asociación privada), OBISAL (sin norma) y Gestión del agua (plataforma del RD 1085/2024). El motivo de cada uno está en `AL1.json` a `AL3.json`.

**Verificación.** Un revisor que no participó en la búsqueda volvió a la fuente de las 10 ([encargo 31](../investigacion/encargos/31-verificar-las-altas.md)). Seis coinciden en todo; en una de ellas (Salud de las Mujeres) con precisiones de redacción, que se han incorporado. En las otras cuatro corrigió la fecha del Observatorio Militar (04/03/2005, la del acuerdo, no la de las órdenes que lo publican), la norma de creación del de Servicios Portuarios (Ley 48/2003, por eso entra por su constitución en 2012) y la forma de redactar las dos creaciones sin acto localizado (RTVE y Vivienda Turística).

**Cómo se aplican.** [`scripts/preparar_altas.py`](../scripts/preparar_altas.py) lee lo que devolvieron los agentes, aplica una a una las correcciones del verificador y las de método (fuera las URL de prensa) y escribe `datos/entrada/altas_2026-10-14.json`. `apply.py` añade esas filas al final de la Hoja 1, con fondo verde. [`scripts/inventario.py`](../scripts/inventario.py) dice qué fichas forman el inventario; las clasificaciones y la comprobación final lo usan para no depender de un número fijo de filas.

## Problemas encontrados y cómo se resolvieron

- **El agente solo puede leer páginas que hayan salido en una búsqueda.** Si pide una URL directa, la herramienta la rechaza. Por eso los encargos dicen que hay que buscar primero el documento.
- **Los PDF largos (leyes de presupuestos, informes de la IGAE) se cortan.** Hay que leerlos por tramos y pedir la cita literal de la fila, no un resumen. En la IGAE, el gasto por capítulos está en miles de euros.
- **Las URL del BOE con «?id=» devolvían a veces otro documento** cuando varios agentes trabajaban a la vez. Hay que comprobar siempre que el título coincide; el verificador detectó un caso (ID 96).
- **Hay un cupo de búsquedas compartido entre agentes simultáneos.** Se repartió en unas 30 búsquedas por agente.
- **Algún agente escribió en columnas que no debía tocar.** `apply.py` protege ID, «URL del documento», «Fecha de revisión» y «Fuentes de la ficha»: las URL nuevas se añaden a «Fuentes de la ficha» sin borrar las anteriores.

## Repetir o ampliar

1. Copia el encargo que corresponda de `investigacion/encargos/` y cambia el lote. Para entidades nuevas, usa los encargos 28 a 31 y `preparar_altas.py` como modelo: un fichero de altas nuevo en `datos/entrada/`, añadido a la lista `ALTAS` de `scripts/inventario.py`, y una entrada por ID en las tres clasificaciones. No toques la hoja original.
2. Dáselo a un agente con búsqueda web, o síguelo a mano. Las reglas valen igual para una persona.
3. Guarda el JSON en `datos/resultados/` y añádelo a la lista `ORDEN` de `scripts/apply.py`, antes de `Z_clasificacion.json`.
4. Ejecuta `python scripts/run_all.py` y revisa en la hoja «Cambios» qué ha cambiado.
5. Antes de dar por buena una tanda, pide a otro agente o a otra persona que coteje una muestra con la fuente, como en el encargo 14.

Para actualizar a otro año o corte, por ejemplo la ejecución a 31/12/2026:
- cambia `REV_DATE` y el literal `CUT` en `apply.py`;
- cambia las fechas de corte en `BRIEF.md`.
