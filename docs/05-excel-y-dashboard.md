# 5. Excel y dashboard

## Excel

`scripts/apply.py` parte siempre de la hoja original de `datos/entrada/`, así que se puede ejecutar las veces que haga falta. Por esa misma razón necesita **todos** los resultados a la vez: los datos de la investigación viven en `datos/resultados/`, no en el Excel. Sin argumentos usa la lista completa (`ORDEN`). Si se le pasa solo una parte, se niega a seguir, porque se perderían datos; solo acepta un Excel parcial con `--parcial`. Lo normal es no llamarlo a mano y usar `python scripts/run_all.py`.

Hace lo siguiente:

1. Aplica los JSON de `datos/resultados/` en orden; la clasificación va la última.
2. Marca **en amarillo** cada celda cambiada y pone la fecha de revisión en la fila.
3. Añade las URL nuevas a «Fuentes de la ficha», sin borrar las anteriores.
4. Añade columnas nuevas al final de «Hoja 1»: la clasificación (útil o no, veredicto, base en el P100, destino, función, duplicidad, UE, actividad, motivo, tema), el coste de apoyo, el coste por persona y el desglose de personal.
5. Crea o rehace estas hojas:

| Hoja | Contenido |
|---|---|
| Entidades | Resumen con fórmulas: presupuesto por base, ejecución de personal a 31/08, cobertura de campos, recuentos por veredicto, por útil o no y por función, base en el P100, texto del criterio y escenario de coste de los órganos consultivos |
| Duplicidades por tema | Matriz tema × territorio con nombre y fuente de cada celda |
| Hoja 1 | La hoja original completada |
| Cambios 12-10-2026 | Cada celda cambiada: valor anterior y valor nuevo |
| Verificación y pendientes | Por ficha: cómo se verificó y qué sigue sin cifra |
| Gasto CNMC y CSIC | Capítulos y a qué se destina cada uno |

Las fórmulas se calculan al abrir el fichero. Si hace falta el fichero con los valores ya calculados (por ejemplo, para leerlo con pandas), ábrelo y guárdalo en Excel o LibreOffice.

`scripts/export_csv.py` saca un CSV plano con una fila por entidad, para leerlo en GitHub o en cualquier hoja de cálculo.

## Dashboard

El dashboard publicado es un artifact de Claude de tipo «Dashboard». El tipo pone el entorno: el objeto `dash`, los estilos (`--cds-*`, `--color-*`) y d3. Nosotros ponemos la página y los datos.

| Fichero | Qué es |
|---|---|
| `dashboard/style.css` | Estilos propios |
| `dashboard/body.html` | Marcado de las seis pestañas: Resumen, Duplicidades, Todas las entidades, Personal, Indicadores, Verificación y pendientes |
| `dashboard/calcs.js` | Todas las cifras derivadas (`dash.calc`): recuentos por veredicto, por útil o no, por base, por presidencia; destino de las integraciones; escenario de coste; indicadores… |
| `dashboard/app.js` | Dibujo de tablas y gráficos con d3, filtros y ficha de detalle |
| `dashboard/datos/*.json` | Los ocho conjuntos de datos que usa la página (los siete de siempre más `referencias_matriz`, las filas de referencia de los organismos de destino) |
| `dashboard/vendor/d3.min.js` | d3 7.9.0, idéntico al publicado en npm, para que la vista previa funcione sin internet |

Los datos salen de `scripts/build_dash_data.py` (que lee el Excel) y de `scripts/clasificacion2.py` (duplicidades y temas). `scripts/build_dashboard.py` monta dos ficheros:
- `dashboard/index.html`: la página tal como se publica en el artifact.
- `dashboard/preview.html`: una copia autónoma que se abre en cualquier navegador. Lleva los datos dentro, carga d3 desde `dashboard/vendor/d3.min.js` e incluye un sustituto mínimo de `dash` y unos estilos de reserva. Sirve para revisar el contenido sin Claude; no reproduce exactamente el aspecto publicado.

Para verlo en local basta con abrir `dashboard/preview.html` en el navegador. Si el navegador bloquea los ficheros locales, sírvelo desde la raíz del repositorio con `python -m http.server 8766` (en Windows también con `.\scripts\serve_dashboard.ps1`) y abre `http://localhost:8766/dashboard/preview.html`.

`python scripts/validate_dashboard_data.py` comprueba los conjuntos de datos y su conexión con los cálculos. También avisa si el Excel se generó sin los resultados de la investigación: menos presupuestos que la hoja original o desglose de personal vacío. `run_all.py` lo ejecuta al final.

### Publicar o actualizar el dashboard en Claude

1. Sube cada `dashboard/datos/<conjunto>.json` como fichero (asset) del artifact (`entidades`, `referencias_matriz`, `personal_desglose`, `csic_personal`, `verificacion_muestra`, `gasto_capitulos`, `duplicidades`, `temas`).
2. Apunta el documento `datasets/<conjunto>` a la URL del fichero subido (los ocho nombres deben coincidir exactamente).
3. Sustituye el documento `files/index.html` por el contenido de `dashboard/index.html` generado por `python scripts/build_dashboard.py` (no edites el HTML a mano).

Lo más sencillo es pedírselo a Claude con este README delante.

**Si en Claude ves «No se pudo cargar» o KPIs en «—»:** casi siempre falta un dataset en el artifact o `index.html` no coincide con el código actual. Compara con `preview.html` local; ver [AUDITORIA_DASHBOARD.md](AUDITORIA_DASHBOARD.md).

**No abras `dashboard/index.html` en el disco:** fuera del artifact no hay `dash`, d3 ni JSON; usa solo `preview.html` o el servidor local.

### Marcado

Para que las cifras se puedan citar y comprobar, la página no lleva números escritos a mano. Cada valor está marcado con `data-source` (el conjunto o el cálculo), `data-field` (la columna) y `data-where` o `data-row` (la fila). Las tablas llevan `data-row-key`. Si se añade una cifra, debe salir de un conjunto o de un `dash.calc`, nunca escrita en el HTML.
