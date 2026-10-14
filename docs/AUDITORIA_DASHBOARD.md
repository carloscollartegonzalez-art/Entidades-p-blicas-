# Auditoría del dashboard (13/10/2026)

Repositorio auditado: fork [adelgadoIAG/Entidades-p-blicas-](https://github.com/adelgadoIAG/Entidades-p-blicas-).

## Resumen ejecutivo

Los errores observados en el **artifact Claude** encajan con un patrón claro: el runtime de Claude Dashboard solo ejecuta `dashboard/index.html` y espera que **siete conjuntos de datos** y **d3** los aporte el entorno. Si falta un dataset, la UI muestra «No se pudo cargar» o KPIs en «—» (`failLine` / `dash-skeleton` en `dashboard/app.js`).

La vista local de referencia es **`dashboard/preview.html`**, generada por `scripts/build_dashboard.py`, que incluye un stub de `dash` y los datos inlined. Tras esta auditoría, el preview usa **d3 local** (`dashboard/vendor/d3.min.js`) para no depender de red.

## Checklist publicación en Claude

Antes de dar por bueno el dashboard publicado:

| Paso | Comprobación |
|------|----------------|
| 1 | Subir los 8 JSON de `dashboard/datos/` como assets del artifact |
| 2 | Enlazar `datasets/entidades`, `referencias_matriz`, `personal_desglose`, `csic_personal`, `verificacion_muestra`, `gasto_capitulos`, `duplicidades`, `temas` a cada asset |
| 3 | Sustituir `files/index.html` por el `dashboard/index.html` generado (no editar a mano) |
| 4 | Tras cambiar datos o `app.js`/`calcs.js`, volver a ejecutar `python scripts/build_dashboard.py` y repetir 1–3 en el mismo paso |
| 5 | Probar las seis pestañas; en consola no debe haber `dash.data(...).status === 'error'` |

**No usar `index.html` abriendo el fichero en disco** (sin Claude): no trae `dash`, d3 ni datasets.

## Validación local realizada

| Comprobación | Resultado |
|--------------|-----------|
| Filas en `entidades.json` | 125 (coherente con README) |
| Reparto veredictos | Antes de la revisión: Mantener 25, Reformar 6. Después (confederaciones a Mantener): Mantener 27, Reformar 4. Integrar 34, Suprimir 43, Pendiente 4 y Extinguida 13, sin cambios |
| `python scripts/build_dashboard.py` en Windows | Fallaba con `UnicodeDecodeError` (cp1252); corregido con `encoding='utf-8'` en el builder |
| `python scripts/validate_dashboard_data.py` | Debe pasar tras regenerar `preview.html` |
| Preview servido con `python -m http.server 8766` (o `scripts/serve_dashboard.ps1` en Windows) | `http://localhost:8766/dashboard/preview.html` |

## Hallazgos técnicos (código)

| Prioridad | Hallazgo | Mitigación aplicada |
|-----------|----------|---------------------|
| Alta | Artifact sin los 7 datasets o `index.html` desactualizado | Checklist arriba; ampliado `docs/05-excel-y-dashboard.md` |
| Media | Preview dependía de CDN cdnjs | `dashboard/vendor/d3.min.js` + script local en preview |
| Media | `build_dashboard.py` sin UTF-8 en Windows | `read_text`/`write_text` con `encoding='utf-8'` |
| Media | Gráficos no se redibujaban al redimensionar | `resize` debounced → `render()` en `app.js` |
| Baja | Hash `#duplicidades` solo al cargar | `hashchange` en `app.js` |
| Baja | `preview.html` desincronizado si se editan fuentes | Ejecutar siempre `build_dashboard.py`; validador en CI/local |
| Alta | Pestañas cambian el subrayado pero no el contenido | `.ep-page { display: grid }` anulaba `[hidden]`; regla `.ep-page[hidden] { display: none !important; }` |

## Comparación artifact vs preview

No se tuvo acceso al artifact concreto de Carlos en esta sesión. Para comparar:

1. Abrir el artifact en Claude y anotar pestañas/bloques con «No se pudo cargar».
2. Abrir el mismo flujo en `preview.html` servido por HTTP.
3. Si el preview está bien y el artifact no, la causa es casi seguro **despliegue** (pasos 1–3 del checklist), no la lógica de `calcs.js`.

## Huecos de datos (no son bugs de UI)

Ver [06-limites-y-pendientes.md](06-limites-y-pendientes.md): 93 celdas de duplicidades sin verificar, desglose de personal incompleto en 22 fichas, etc. El dashboard refleja esos vacíos con «—» o notas, no con errores de JavaScript.

## Comandos útiles

Desde la raíz del repositorio (Windows, macOS o Linux):

```
python -m pip install -r requirements.txt
python scripts/run_all.py          # regenera todo y valida al final
python -m http.server 8766         # y abrir http://localhost:8766/dashboard/preview.html
```
