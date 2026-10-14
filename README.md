# Entidades públicas: poder, presupuesto y utilidad

Un análisis de Iniciativa Extramuros.

Análisis de las 125 entidades públicas españolas creadas o transformadas desde 2006: 69 estatales, 3 creaciones legales no constituidas y 53 autonómicas. Es un inventario parcial.

Para cada entidad se recogen tres cosas:
- **Cuánto cuesta:** presupuesto propio, gasto de personal y plantilla, siempre con fuente oficial.
- **Si es útil según el P100 de Extramuros.**
- **Cuántos organismos hacen lo mismo** entre el Estado y las 17 comunidades autónomas.

La carpeta contiene todo lo necesario para que otra persona pueda:
1. consultar los resultados;
2. reproducirlos desde la hoja original;
3. ampliarlos o actualizarlos con el mismo método.

Fecha de corte: 12/10/2026. Las cifras de ejecución de 2026 llegan hasta el 31/08/2026 (IGAE).

## Resultado

| Veredicto | Entidades | Con presupuesto propio 2026 | Presupuesto propio 2026 (M€, orden de magnitud) |
|---|---|---|---|
| Mantener | 27 | 25 | 9.099 |
| Reformar | 4 | 4 | 1.103 |
| Integrar en otro organismo | 34 | 27 | 2.264 |
| Suprimir | 43 | 2 | 77 |
| Pendiente de decisión (el P100 no trata la materia) | 4 | 1 | 81 |
| Extinguida | 13 | 0 | 0 |

- **Útiles (Mantener + Reformar): 31.** No útiles (Integrar + Suprimir): 77.
- **Útil no es tener un contenido, sino a qué sirve ese contenido.** Un organismo es útil solo si:
  - su función es necesaria;
  - nadie más la presta (con uno nacional basta);
  - sirve a un fin del P100.
- El criterio completo está en [docs/03-clasificacion-p100.md](docs/03-clasificacion-p100.md).
- Los presupuestos suman créditos de bases distintas. Valen como orden de magnitud, no como total contable.

Más resultados:
- **Duplicidades:** en 13 temas hay 10 o más organismos verificados entre el Estado y las comunidades. Por ejemplo, 15 observatorios de convivencia escolar y 13 consejos de transparencia.
- **Órganos consultivos:** no tienen presupuesto propio, pero sí coste de personal. Son entre 2,2 y 6,7 M€ al año para los 40 órganos, según los ocupe 1, 2 o 3 personas (escenario, no dato publicado).
- **CNMC:** solo el 1,7% de su presupuesto es funcionamiento propio. El resto pasa a terceros por mandato legal.
- **CSIC:** el 40% es personal. Tiene 7.465 científicos y 1.139 personas de gestión.

## Por dónde empezar

| Si quieres… | Abre |
|---|---|
| Ver el resultado entidad por entidad | [`salida/clasificacion_entidades.csv`](salida/clasificacion_entidades.csv) (GitHub lo muestra como tabla) |
| La hoja completa, con fuentes, cambios y verificación | [`salida/Entidades_publicas_poder_y_presupuesto_v5.xlsx`](salida/) |
| Ver el dashboard sin Claude | Descarga el repositorio y abre [`dashboard/preview.html`](dashboard/preview.html) en el navegador; si no carga, `python -m http.server 8766` y abre `http://localhost:8766/dashboard/preview.html` (no uses `index.html` en local) |
| Entender cómo se hizo | [`docs/`](docs/), en este orden |
| Cambios y revisiones posteriores | [`docs/REVISIONES_Y_CAMBIOS.md`](docs/REVISIONES_Y_CAMBIOS.md) |
| Reproducirlo | `python scripts/run_all.py` (ver abajo) |

## El proceso en seis pasos

1. **Método de datos.** Cifras en millones de euros, con año, base y corte explícitos. Solo fuentes oficiales. Nunca un 0 por «no encontrado» y nunca una estimación en una columna de datos. → [docs/01-metodo-de-datos.md](docs/01-metodo-de-datos.md)
2. **Investigación.** 27 encargos a agentes de investigación (Claude), por lotes de entidades y en dos rondas. Cada encargo devuelve un JSON con las celdas que cambian, sus fuentes y cómo se verificó. Un revisor independiente cotejó una muestra de 20 cifras con la fuente. → [docs/02-investigacion.md](docs/02-investigacion.md)
3. **Clasificación según el P100.** Seis veredictos, cada uno con su base en el P100 («explícito» o «aplicando el criterio») y el destino de las funciones. → [docs/03-clasificacion-p100.md](docs/03-clasificacion-p100.md)
4. **Duplicidades Estado + comunidades.** 21 temas, con una celda por territorio y su fuente. → [docs/04-duplicidades.md](docs/04-duplicidades.md)
5. **Volcado al Excel y dashboard.** Los scripts aplican los JSON a la hoja original, marcan en amarillo cada celda cambiada, registran el cambio y generan los datos del dashboard. → [docs/05-excel-y-dashboard.md](docs/05-excel-y-dashboard.md)
6. **Límites y pendientes.** Lo que no está verificado y lo que falta. → [docs/06-limites-y-pendientes.md](docs/06-limites-y-pendientes.md)

## Reproducir

Requisitos: Python 3.10 o superior y `openpyxl` (`pip install -r requirements.txt`).

```
python scripts/run_all.py
```

Funciona igual en Windows, macOS y Linux; en macOS y Linux también vale `bash scripts/run_all.sh`. El script hace todo el recorrido a partir de la hoja original (`datos/entrada/`) y de los resultados de la investigación (`datos/resultados/`):
- rehace las tres clasificaciones;
- genera el Excel en `salida/`;
- produce los datos y las páginas del dashboard;
- exporta el CSV;
- comprueba al final que no falta nada (`scripts/validate_dashboard_data.py`).

No ejecutes `apply.py` a mano con solo algunos ficheros de resultados: reconstruye el Excel desde la hoja original y perderías los datos que no le pases. Por eso se niega a hacerlo.

No consulta internet. La investigación ya está hecha y guardada en `datos/resultados/`. Para rehacerla o ampliarla, ver [docs/02-investigacion.md](docs/02-investigacion.md).

El Excel que genera el script trae las fórmulas sin calcular; se calculan al abrirlo. La copia que hay en `salida/` ya está recalculada.

## Estructura

```
extramuros-entidades-publicas/
├── README.md
├── requirements.txt
├── docs/                      método, investigación, criterio P100, duplicidades, Excel y dashboard, límites
├── datos/
│   ├── entrada/               hoja original de 125 entidades (sin tocar)
│   ├── resultados/            JSON de cada encargo de investigación y de cada clasificación
│   ├── referencias_matriz.json  organismos de destino que no están entre las 125 (solo como referencia)
│   └── matrices_en_inventario.json  destinos que sí tienen ficha propia
├── investigacion/
│   ├── BRIEF*.md              instrucciones comunes de los encargos (método, columnas, formato)
│   ├── headers.json, ejemplos.json, verificar.json
│   ├── lotes/                 qué entidades y campos recibió cada encargo
│   ├── encargos/              texto literal de los 27 encargos
│   ├── scripts-agentes/       scripts que escribieron los agentes para generar sus resultados
│   └── notas/                 notas de trabajo de los agentes
├── scripts/
│   ├── run_all.py             todo el proceso (run_all.sh es un atajo para macOS/Linux)
│   ├── clasificacion.py       v1 (histórica): niveles A-D
│   ├── clasificacion2.py      v2: función, tema, duplicidad, UE, actividad
│   ├── clasificacion3.py      v3: veredicto alineado con el P100 (la vigente)
│   ├── apply.py               vuelca los JSON en la hoja y crea las hojas de resumen
│   ├── build_dash_data.py     datos del dashboard
│   ├── destino_labels.py      nombres completos de los organismos de destino
│   ├── build_dashboard.py     página del dashboard y vista previa
│   ├── export_csv.py          CSV plano de la clasificación
│   ├── validate_dashboard_data.py  comprobaciones finales (datos completos, cálculos)
│   └── serve_dashboard.ps1    servidor local para la vista previa en Windows
├── dashboard/                 código del dashboard (estilo, marcado, cálculos, dibujo), sus datos y d3 en vendor/
└── salida/                    Excel v5 y CSV
```
