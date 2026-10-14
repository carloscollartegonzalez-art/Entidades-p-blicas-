# Brief: altas de entidades nuevas en «Entidades públicas: poder y presupuesto»

## Contexto
La hoja tiene 125 entidades públicas españolas (estatales y autonómicas) **creadas o transformadas desde 2004** (periodos Zapatero, Rajoy y Sánchez). Se van a añadir observatorios estatales que faltaban. Para cada candidato de tu lote tienes que decidir si entra y, si entra, rellenar su ficha completa con el mismo método que el resto de la hoja.

Ficheros (léelos con Read):
- `investigacion/headers.json`: las 73 cabeceras exactas de la Hoja 1.
- `investigacion/ejemplos_altas.json`: tres fichas completas ya hechas. ID9 (Observatorio de la Vida Militar) y ID60 (Observatorio de Derechos Digitales) son órganos sin presupuesto propio, el caso más habitual en este lote; ID3 es una agencia con presupuesto. Copia su estilo, vocabulario y nivel de detalle.
- Tu lote (indicado en el encargo): los candidatos con pistas. Las pistas son orientativas: verifícalas en la fuente oficial.

## Cuándo entra un candidato (las tres condiciones)
1. **Es sector público estatal:** un órgano (colegiado o unidad con nombre propio) o una entidad de la Administración General del Estado, de sus organismos o de sus sociedades, o creado por una ley estatal. No entran proyectos de universidades, fundaciones privadas, asociaciones, colegios profesionales ni redes financiadas por subvención o convenio sin norma que los cree.
2. **Se creó o se transformó desde el 17/04/2004** (inicio del Gobierno Zapatero): creación, recreación, cambio de nombre con nueva regulación o constitución efectiva. Si se creó antes y no ha cambiado, no entra.
3. **Hay un acto oficial que lo crea o lo aprueba:** ley, real decreto, orden, acuerdo del Consejo de Ministros, resolución, o un anteproyecto o proyecto de ley aprobado por el Consejo de Ministros. Si solo está aprobado o anunciado y no constituido, entra con «Estado legal y operativo» = creación anunciada o en tramitación, no constituido (como las 3 «creaciones legales de constitución no confirmada» que ya hay en la hoja).

No entran series estadísticas, informes periódicos, portales web o herramientas sin órgano detrás, aunque se llamen «observatorio».

## Reglas de método (obligatorias, las mismas de la hoja)
1. Solo fuentes primarias u oficiales: BOE, boletines, leyes y anexos de presupuestos, IGAE, webs oficiales de ministerios y organismos, memorias oficiales, Moncloa. La prensa solo sirve como pista.
2. Cada dato con URL y localización (artículo, página). Cifras en millones de EUR, hasta 6 decimales.
3. Nunca estimar, nunca prorratear el presupuesto de un ministerio, nunca poner 0 por «no encontrado».
4. Órganos sin personalidad: busca en la norma si dice «no supondrá incremento del gasto», «se atenderá con los medios del Ministerio» o «los miembros no percibirán retribución». Si es así, pon **Estado de cuantificación** = `Sin presupuesto propio: órgano sin dotación diferenciada (verificado en norma)` y explica el artículo en «Presupuesto: texto completo», «Notas de personal y apoyo ministerial» y «Cobertura presupuesto / personal / salarios». Si un importe concreto lo financia (convenio, contrato, encargo), va en las columnas contextuales («Importe contextual (EUR millones; NO sumar)», «Año / periodo contextual», «Base contextual», «Nombre del titular del importe»), nunca como presupuesto propio.
5. Vocales y miembros no son plantilla. Si la norma fija una unidad de apoyo, un secretario o dietas, anótalo en «Notas de personal y apoyo ministerial».
6. **Periodo presidencial** según la fecha del acto que lo crea o transforma: `Zapatero` (17/04/2004–20/12/2011), `Rajoy` (21/12/2011–01/06/2018), `Sánchez` (desde 02/06/2018).
7. **Ámbito** = `Estatal`; **Comunidad autónoma** = `Estado`. No rellenes `ID` ni `URL del documento`; pon `Fecha de revisión` = `14/10/2026`.
8. Rellena también las columnas de juicio (Poder real, Duplicidades, Papel en leyes, Informe obligatorio, Informe vinculante, Bloqueo o demora, Norma / artículo sobre consulta, Fuente legal de consulta normativa), con el mismo tipo de frase prudente que los ejemplos. Si el órgano emite informes **preceptivos**, dilo expresamente.

## Acceso web
- Usa WebSearch (mode "standard"; "extended" solo si lo estándar sale pobre) y WebFetch. **WebFetch solo funciona con URLs que hayan salido en resultados de WebSearch**; si da PROVENANCE_REQUIRED, busca el documento para que su URL aparezca.
- El cupo de búsquedas se comparte con otros dos agentes: **máximo unas 30 búsquedas en total**.
- Si una URL del BOE con «?id=» devuelve un documento de otro título, descártala. Prefiere las URL ELI (`boe.es/eli/...`) o `boe.es/buscar/doc.php?id=`.
- PDFs largos: usa `offset` y pide la cita literal del artículo.

## Salida
Escribe un JSON (lista, una entrada por candidato de tu lote, entre o no) en la ruta del encargo:
```json
[
  {
    "candidato": "nombre tal como viene en el lote",
    "incluir": true,
    "motivo": "por qué entra o no (condiciones 1-3), con la norma y la fecha",
    "fila": {"<cabecera exacta de headers.json>": "<valor>", "...": "..."},
    "apoyo": {"unidad_apoyo": "...", "puestos_asignados": "...", "vocales": "...", "retribucion_miembros": "...", "gasto_identificable": "...", "fuente": "https://..."},
    "fuentes": ["https://..."],
    "verificacion": "para cada dato: documento, artículo o página",
    "no_encontrado": "qué buscaste y no apareció"
  }
]
```
- Si `incluir` es false, deja `fila` y `apoyo` vacíos ({}).
- En `fila`, usa las cabeceras **exactas** de headers.json y pon en «Fuentes de la ficha» las URL separadas por saltos de línea.
- Valida el JSON con `python3 -c "import json; json.load(open(RUTA))"`.

Respuesta final: un resumen breve (máx. 12 líneas) de qué candidatos entran, cuáles no y por qué, y cualquier duda.
