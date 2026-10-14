# Revisiones y cambios (fork / mantenimiento)

Registro de cambios metodológicos o de datos hechos **después** de la publicación original del análisis (corte 12/10/2026). Cada entrada debe indicar qué se cambió, por qué y qué validación se hizo.

## 2026-10-14 — Corte desde 2004 y 10 observatorios estatales que faltaban

- **Corte: desde 2004, no desde 2006.** La documentación decía «creadas o transformadas desde 2006», pero la hoja original va desde el 17/04/2004 (inicio del Gobierno Zapatero): la ficha más antigua es de octubre de 2004. Se corrige en el README, los documentos, el dashboard y el motivo de las confederaciones hidrográficas. El P100 (Costes del Estado 9) usa el mismo corte.
- **10 altas (IDs 126 a 135).** Al cruzar el inventario con el catálogo de observatoriospublicos.es salieron 51 observatorios del Estado que no estaban. Se investigaron 21 (encargos 28 a 30) y entran 10; un revisor independiente comprobó los 10 (encargo 31). Detalle y criterio de entrada en [02-investigacion.md](02-investigacion.md#altas-del-14102026).
  - Inventario: 135 fichas (76 estatales, 3 creaciones legales no constituidas, 3 creaciones anunciadas o en tramitación y 53 autonómicas).
  - Veredictos: Mantener 28 (+1, Observatorio Nacional de Seguridad Vial), Suprimir 52 (+9). Útiles 32; no útiles 86.
  - Base en el P100: explícitos 63 (+8), deducciones 55 (+2).
  - Órganos consultivos: 46 (+6). El escenario de coste pasa a 2,6–7,8 M€ al año.
  - Ninguna alta tiene presupuesto propio: los totales de presupuesto no cambian.
- **Código:**
  - `scripts/preparar_altas.py` construye las fichas a partir de lo que devolvieron los agentes y aplica, una a una y con su motivo, las correcciones del verificador y las de método (fuera las URL de prensa).
  - `scripts/inventario.py` dice qué fichas forman el inventario. Las clasificaciones y el validador ya no dependen de 125 filas fijas.
  - `apply.py` añade las altas al final de la Hoja 1 con fondo verde y amplía hasta la última fila los rangos de las fórmulas de la hoja «Entidades».
  - `clasificacion2.py` lee el coste de apoyo de todos los `C_apoyo*.json`.
  - El Excel pasa a llamarse `..._v6.xlsx`.
- **Validación:**
  - `python scripts/run_all.py` completo y el validador en OK (135 filas).
  - Excel recalculado sin errores (276 fórmulas).
  - Las 125 fichas originales no cambian salvo el motivo de las confederaciones (2004 en vez de 2006): 2.712 celdas cambiadas, las mismas que antes.

---

## 2026-10-14 — Versión corregida sobre la revisión del 13/10

Se incorporan los cambios del PR #1 (pestañas, nombres completos de destinos, columna de matriz, nota del 112, filas de referencia, d3 local, UTF-8) y se corrige lo siguiente.

- **Datos de la investigación restaurados.** En el PR #1 el Excel se regeneró llamando a `apply.py` solo con `Z_clasificacion.json`. Como `apply.py` parte siempre de la hoja original, se perdieron los resultados de la investigación:

  | Dato | Antes | En el PR #1 |
  |---|---|---|
  | Presupuestos | 61 | 38 |
  | Personas | 29 | 4 |
  | Desglose de personal | 29 | 0 |
  | Celdas cambiadas | 2.712 | 1.242 |

  Se ha regenerado todo con el proceso completo y vuelven las cifras de antes.
- **Para que no vuelva a pasar:**
  - `apply.py` usa la lista completa si no recibe ficheros y se niega a seguir si faltan resultados (salvo `--parcial`).
  - `validate_dashboard_data.py` falla si hay los mismos presupuestos que en la hoja original o si el desglose de personal está vacío.
  - Nuevo `scripts/run_all.py` para Windows, macOS y Linux, con UTF-8 forzado. `run_all.sh` queda como atajo.
  - Todas las lecturas de JSON llevan `encoding='utf-8'`.
- **Confederaciones hidrográficas: se acepta Mantener.** El argumento de coherencia es este: la medida 12 de «Menos normas» cambia el procedimiento de informes de todos los organismos que informan planes, igual que la medida 9 de Costes a la CNMC o la AIReF, que están en Mantener. Reformar queda para los organismos a los que el P100 cambia a ellos mismos (CTBG, AECID, INVIED, SETT). La base pasa a «Aplicando el criterio»: explícitos de 57 a 55, deducciones de 51 a 53.
- **Filas de referencia (9001–9008):**
  - siguen fuera de todos los totales;
  - en la tabla, su importe lleva el año: «1.231,6 (2023)»;
  - una nota explica que son de 2023 y de bases distintas.

  Comprobado en el ROM citado: la cifra de la AEAT (1.231,6 M€) es la transferencia corriente de Hacienda, no su presupuesto total.
- **d3 local:** `dashboard/vendor/d3.min.js` es idéntico byte a byte a d3 7.9.0 de npm.
- **Fechas corregidas** (las entradas decían 12/03/2026) y **rutas locales retiradas** de la documentación.
- **Validación:**
  - `python scripts/run_all.py` completo y el validador en OK.
  - Excel recalculado sin errores (266 fórmulas).
  - Frente a `main`, la hoja solo cambia en veredicto, base y motivo de las confederaciones, en los motivos de las tres agencias de emergencias y en los nombres completos de los destinos.
  - Vista previa probada en el navegador: cada pestaña muestra solo su panel, Personal tiene sus 29 filas y no hay errores en la consola.

---

## 2026-10-13 — Dashboard: pestañas, matriz de integración y UI

| Área | Cambio | Motivo |
|------|--------|--------|
| CSS / `app.js` | Pestañas no ocultaban paneles | `.ep-page { display: grid }` anulaba `[hidden]` |
| Tabla entidades | Columna «Matriz / integración» | Mostrar `destino` sin abrir el detalle |
| Tema 112 | Nota en tabla y en Duplicidades | No hay organismo estatal que absorba el 112 |
| Docs | `AUDITORIA_DASHBOARD.md`, `serve_dashboard.ps1`, d3 local | Revisión local y publicación Claude |

**Validación:** `python scripts/build_dashboard.py`, `python scripts/validate_dashboard_data.py`, servidor local.

---

## 2026-10-13 — Clasificación, destinos y referencias (revisión metodológica)

### 1. Agencia de Emergencias de Andalucía (id 101) — sigue **Mantener**

- **Pregunta:** ¿Debería ser «Integrar» por el «mando único» (112, GREA, IESPA)?
- **Decisión:** **No.** El veredicto «Integrar» del P100 significa que la función pasa a un **organismo estatal** (o equivalente nacional) porque «con uno basta». El 112 es competencia autonómica; el Estado no presta el servicio en ninguna CCAA (`temas.json`, tema «Entes de emergencias 112»).
- **Cambio:** Se amplía el **motivo** en `clasificacion3.py` para distinguir integración operativa interna de la CA del veredicto P100.
- **Indicadores:** Sigue apareciendo «Mantener» porque el veredicto no cambia; es coherente con Asturias y Cantabria (mismo tema).

### 2. Confederaciones hidrográficas Miño-Sil (37) y Cantábrico (38) — **Mantener** (antes Reformar)

- **Pregunta:** ¿Por qué solo estas dos y «Reformar»? ¿Y Ebro, Tajo, etc.?
- **Decisión:** Son **organismos autónomos estatales** adscritos al ministerio de Medio Ambiente, no duplicidades autonómicas. El inventario de 125 solo incluye entidades **creadas o transformadas desde 2004** (decía 2006 por error; corregido el 14/10/2026); otras confederaciones no tienen ficha en esta hoja.
- **P100 «Menos normas 12»:** Afecta al régimen de informes (silencio favorable), no a suprimir o integrar el organismo. Se reclasifican como **Mantener** con motivo explícito.
- **Efecto en cifras:** «Reformar» pasa de 6 a **4** (quedan CTBG, AECID, INVIED, SETT) y «Mantener» de 25 a **27**. Útiles siguen siendo 31.

### 3. Nombres completos en «destino / matriz»

- **Cambio:** `scripts/destino_labels.py` y aplicación en `clasificacion3.py` + `build_dash_data.py` (`destino_mostrar`).
- **Motivo:** Siglas (CDTI, AEAT, CNMC…) generan dudas en lectura no experta.

### 4. Matrices de integración en «Todas las entidades»

- **Problema:** Destinos del P100 (CDTI, AEAT, ANECA…) no tenían ficha en las 125 entidades.
- **Cambio:** Filas de **referencia** en `datos/referencias_matriz.json` → `dashboard/datos/referencias_matriz.json` (veredicto «Referencia»), **excluidas** de KPIs e `indicadores` en `calcs.js`.
- **Matrices que ya están en el inventario** (no se duplican): AEI id 4, AIReF id 5, CTBG id 6, CNMC id 24 — listado en `datos/matrices_en_inventario.json`.
- **Presupuesto PGE 2023** (miles € → M€ en el dashboard), donde hay fuente ROM u oficial:

| id ref. | Organismo | presupuesto_m (2023) | Fuente principal |
|--------|-----------|----------------------|------------------|
| 9001 | CDTI | 1.086,9 | [POA CDTI 2023](https://www.cdti.es/sites/default/files/2023-06/poa_2023_2.pdf); ROM `N_23_E_R_5_0_0N_0_0152_0` (no INNVIERTE `0978`) |
| 9002 | AEAT | 1.231,6 | [ROM Hacienda AEAT](https://www.congreso.es/docu/pge2023/pge_2023-web/PGE-ROM/doc/HTM/N_23_A_R_31_115_1_1_1_T_1.HTM) |
| 9003 | ANECA | **12,9** (total ingresos O.A.; no solo transferencia 8,9) | [ROM OO.AA. ingresos](https://www.sepg.pap.hacienda.gob.es/Presup/PGE2023Ley/MaestroDocumentos/PGE-ROM/doc/HTM/N_23_E_V_1_102_2_1_A_1.HTM) |
| 9004 | AEPD | 18,8 | [Presupuesto AEPD 2023](https://www.aepd.es/documento/presupuestos-aepd-2023.pdf) |
| 9005 | Defensor del Pueblo | 20,9 | [Ejecución 2023](https://www.defensordelpueblo.es/transparencia/informacion-economica-presupuestaria-y-contractual/presupuestos/ejecucion-2023/) |
| 9006 | IDAE | 195,8 (subv. explotación) | [PEC IDAE PGE 2023](https://www.congreso.es/docu/pge2023/pge_2023-web/PGE-ROM/doc/1/6/1/1/22/N_23_A_R_5_0_0N_0_0154_0_PECROOT1_24013.PDF) |
| 9007 | INCIBE | 23,5 (ordinario + socio) | [Cuentas INCIBE 2023](https://www.incibe.es/sites/default/files/paginas/normativa-financiera/2023_informacion_financiera.pdf) |
| 9008 | CCN-CERT | — | Solo ancla institucional (sin ROM limitativo propio) |

- **Pendiente:** Personal y cap. 1 en referencias cuando se extienda el mismo método que las 125 fichas (corte 2026 en inventario).
- **Desglose núcleo técnico/científico vs administración:** solo existe en el pipeline del inventario (`personal_desglose.json`, generado desde el Excel). Las filas `referencias_matriz` **no** tienen ese desglose; (en la primera versión de esta revisión `personal_desglose.json` salía vacío, pero no por eso: el Excel se había regenerado sin los resultados de personal; ver la entrada del 14/10/2026). No se ha replicado el trabajo de clasificación de plantilla para CDTI, AEAT, ANECA, AEPD, Defensor, IDAE ni INCIBE.

### Regenerar datos tras cambios de clasificación

Desde la raíz del repositorio, en cualquier sistema:

```
python scripts/run_all.py
```

No llames a `apply.py` solo con `Z_clasificacion.json`. Reconstruye el Excel desde la hoja original y se perderían todos los resultados de la investigación. Ahora se niega a hacerlo (ver la entrada del 14/10/2026).

---

## Próximos pasos (documentados, sin implementar)

Ideas acordadas para una iteración posterior; **no** forman parte del comportamiento actual del dashboard.

1. **Definición única de «presupuesto» en fichas y referencias**  
   Hoy conviven criterios distintos según el tipo de ente: transferencia nominativa (ANECA cap. 4), dotación PPGGE (CDTI), presupuesto de ingresos/gastos de O.A. (ANECA total ~12,9 M€), PEC de E.P.E. (IDAE con fuerte componente UE), partidas MRR a parte (INCIBE), etc. Convendría un glosario en `docs/` (p. ej. ampliar `REVISIONES_Y_CAMBIOS` o `AUDITORIA_DASHBOARD.md`) con: qué va en `presupuesto_m`, qué en `contextual_m`, año de corte y enlace ROM obligatorio por fila.

2. **Capítulo 1 y personal en `referencias_matriz`**  
   Mismo método que las 125 fichas (IGAE 2026 o PGE según se decida en el punto 1).

3. **Desglose núcleo técnico/científico vs administración**  
   Solo el inventario alimenta `personal_desglose.json` desde el Excel; las referencias 9001–9008 no lo tienen. Opciones: ampliar el libro/plantilla o un script de extracción por organismo (memoria, RPT, transparencia).

4. **Validación automática de referencias**  
   Comprobar que `presupuesto_anio`, `presupuesto_base` y `fuente` HTTPS están rellenos en todas las filas con `referencia_matriz: true`.

---

## Plantilla para próximas entradas

```markdown
## YYYY-MM-DD — Título breve

- **Archivos:** …
- **Decisión / cambio:** …
- **Validación:** …
```
