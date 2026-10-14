"""Rebuilds the workbook: original sheet + new entries (altas) + every research result + the classification.

It ALWAYS starts from datos/entrada/Entidades_publicas_poder_y_presupuesto_final_125.xlsx and appends the
altas listed in scripts/inventario.py (green rows), so the research data only survives if every results
file is applied. With no file arguments it uses the
full list below (ORDEN), which is what scripts/run_all.py does. If you pass a subset it stops,
because that would silently drop data; add --parcial only if you really want a partial workbook.

Usage:
  python scripts/apply.py                    # full rebuild into salida/Entidades_publicas_poder_y_presupuesto_v6.xlsx
  python scripts/apply.py out.xlsx           # full rebuild into out.xlsx
  python scripts/apply.py out.xlsx a.json b.json --parcial   # only these files (data from the others is lost)
Files are applied in the given order; when two touch the same cell, the later one wins.
"""
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent  # raíz del repositorio
RES = BASE / 'datos' / 'resultados'
import sys, json, copy, re
sys.path.insert(0, str(BASE / 'scripts'))
from inventario import altas as _altas
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter as L

SRC = BASE / 'datos' / 'entrada' / 'Entidades_publicas_poder_y_presupuesto_final_125.xlsx'
# Every results file, in the order they must be applied (the classification goes last).
ORDEN = [
    'A_estatal_entes.json', 'B1_estatal_colegiados.json', 'B2_estatal_colegiados.json', 'C_estatal_plantillas.json',
    'D_andalucia_aragon.json', 'E_ast_bal_can_cant.json', 'F_clm_cyl_cat_ext_gal.json', 'G_mad_mur_nav_pv_rio_val.json',
    'R2A_estatal.json', 'R2B_colegiados.json', 'R2C_andalucia_aragon.json', 'R2D_ast_bal_can_cant.json', 'R2E_varias.json',
    'P1_investigacion.json', 'P2_reguladores.json', 'P3_estatal_otros.json', 'P4_andalucia_aragon.json',
    'P5_ast_bal_can_cant_cat.json', 'P6_gal_mad_mur_nav_pv_val.json',
    'Z_clasificacion.json',
]
_args = [a for a in sys.argv[1:] if a != '--parcial']
PARCIAL = '--parcial' in sys.argv[1:]
out = _args[0] if _args else str(BASE / 'salida' / 'Entidades_publicas_poder_y_presupuesto_v6.xlsx')
files = _args[1:] or [str(RES / f) for f in ORDEN]
_missing = [f for f in ORDEN if f not in {Path(x).name for x in files}]
if _missing and not PARCIAL:
    sys.exit('apply.py: faltan ficheros de resultados y se perderían sus datos, porque el Excel se reconstruye '
             'siempre desde la hoja original.\n  Faltan: ' + ', '.join(_missing) +
             '\n  Ejecuta `python scripts/run_all.py` (o `python scripts/apply.py` sin ficheros) para usar la lista completa.'
             '\n  Si de verdad quieres un Excel parcial, añade --parcial.')

REV_DATE = '12/10/2026'
FILL = PatternFill('solid', fgColor='FFFFF2CC')
FILL_ALTA = PatternFill('solid', fgColor='FFE2EFDA')   # rows added after the original sheet

wb = openpyxl.load_workbook(SRC)
ws = wb['Hoja 1']
hdr = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}

# ---- altas: new rows appended after the original ones, with the style of row 2 and a green fill
N_ORIG = ws.max_row - 1
ALTAS = _altas()
alta_ids = set()
for a in ALTAS:
    r = ws.max_row + 1
    for h, c in hdr.items():
        ws.cell(r, c)._style = copy.copy(ws.cell(2, c)._style)
        v = a['fila'].get(h)
        if isinstance(v, str) and v.strip() == '':
            v = None
        ws.cell(r, c).value = v
        if v is not None:
            ws.cell(r, c).fill = FILL_ALTA
    if ws.row_dimensions[2].height:
        ws.row_dimensions[r].height = ws.row_dimensions[2].height
    alta_ids.add(a['ID'])
row_of = {int(float(ws.cell(r, 1).value)): r for r in range(2, ws.max_row + 1)}
LAST = ws.max_row          # last data row of Hoja 1 (row 126 in the original sheet)
N = LAST - 1               # number of entities

# new columns appended after the existing ones (classification first, then staff breakdown)
NEW_COLS = ['Clasificación: útil / no útil', 'Clasificación: veredicto', 'Clasificación: función',
            'Clasificación: duplicidad', 'Clasificación: exigida por la UE', 'Clasificación: actividad reciente',
            'Clasificación: motivo', 'Clasificación: base en el P100', 'Clasificación: destino de sus funciones', 'Tema funcional', 'Organismos del mismo tema (Estado + CCAA, verificados)',
            'Coste de apoyo (sin presupuesto propio): unidad, vocales y dietas',
            'Coste de personal por persona 2025 (EUR, calculado)',
            'Desglose: personal técnico/científico/inspector', 'Desglose: personal de administración y apoyo',
            'Desglose: otro / no clasificable', 'Desglose: total de referencia',
            'Puestos de libre designación', 'Altos cargos', 'Personal eventual (confianza)',
            'Desglose: unidad y fecha', 'Desglose: criterio de clasificación', 'Desglose: fuente',
            'Desglose: verificación']
NEW_NUMERIC = ['Organismos del mismo tema (Estado + CCAA, verificados)', 'Desglose: personal técnico/científico/inspector', 'Desglose: personal de administración y apoyo',
               'Desglose: otro / no clasificable', 'Desglose: total de referencia',
               'Puestos de libre designación', 'Altos cargos', 'Personal eventual (confianza)']
_last = ws.max_column
for h in NEW_COLS:
    if h in hdr:
        continue
    _last += 1
    cell = ws.cell(1, _last, h)
    cell._style = copy.copy(ws.cell(1, _last - 1)._style) if _last - 1 > 73 else copy.copy(ws.cell(1, 73)._style)
    ws.column_dimensions[L(_last)].width = 44 if h in ('Clasificación: motivo', 'Clasificación: base en el P100', 'Clasificación: destino de sus funciones', 'Desglose: criterio de clasificación', 'Desglose: verificación', 'Desglose: unidad y fecha') else 16
    for r in range(2, ws.max_row + 1):
        ws.cell(r, _last)._style = copy.copy(ws.cell(r, 73)._style)
    hdr[h] = _last
ws.auto_filter.ref = f'A1:{L(ws.max_column)}{ws.max_row}'

NUMERIC = ['Presupuesto propio (EUR millones)', 'Año del presupuesto', 'Crédito inicial (EUR millones)',
           'Modificación neta (EUR millones)', 'Importe contextual (EUR millones; NO sumar)',
           'Personal: personas (ocupadas)', 'Crédito de personal (EUR millones)', 'Año del coste de personal',
           'Gasto de personal ejecutado (EUR millones)', 'Año del gasto de personal',
           'Puestos aprobados / presupuestados', 'Pagos de personal 2026 hasta 31/08 (EUR millones)',
           'Crédito personal comparativo2025, edición08.2026 (EUR millones)',
           'Obligaciones personal comparativo2025, edición08.2026 (EUR millones)',
           'Crédito personal inicial / otra base (EUR millones; NO sumar)',
           'Crédito personal 2025 cierre (EUR millones)', 'Gasto personal 2025 reconocido anual (EUR millones)',
           'Pagos personal 2025 anual (EUR millones)'] + NEW_NUMERIC
NEVER_TOUCH = {'ID', 'URL del documento', 'Fecha de revisión', 'Fuentes de la ficha'}

# number formats per column, taken from an existing filled numeric cell
numfmt = {}
for h in NUMERIC:
    c = hdr[h]
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, c).value
        if isinstance(v, (int, float)):
            numfmt[h] = ws.cell(r, c).number_format
            break
for h in NEW_NUMERIC:
    numfmt[h] = '#,##0'

# manual overrides decided in review (ID -> {header: value})
OVERRIDES = {
    102: {'Estado de cuantificación': 'Sin presupuesto propio 2026: no figura en la ley de presupuestos (entidad no desplegada)'},
    59: {'Estado de cuantificación': 'Sin presupuesto propio: órgano sin dotación diferenciada (financiación por convenio, verificada en BOE)'},
    60: {'Estado de cuantificación': 'Sin presupuesto propio: órgano sin dotación diferenciada (financiación por convenio, verificada en BOE)'},
}
U_OLD = 'No se ha verificado el número actual de puestos ocupados ni la independencia práctica de su dirección.'
U_NEW = 'Plantilla ocupada: ver columna de personal (EPSAP enero 2026 o fuente indicada); no se ha verificado la independencia práctica de su dirección.'


def clean(h, v):
    if isinstance(v, str):
        v = v.strip()
        if v == '':
            return None
    if h in NUMERIC and isinstance(v, str):
        s = v.replace(' ', '')
        if re.fullmatch(r'-?\d+(\.\d+)?', s):
            v = float(s) if '.' in s else int(s)
    if isinstance(v, float) and v.is_integer() and h.startswith('Año'):
        v = int(v)
    return v


changes = []      # (ID, name, header, old, new)
notes = {}        # ID -> dict(verificacion, no_encontrado, lote)
extra_sources = {}
for a in ALTAS:
    notes[a['ID']] = {'lote': [a.get('lote') or 'altas'],
                      'verificacion': [f"Alta del 14/10/2026. Por qué entra: {a['motivo_inclusion']}", a['verificacion']],
                      'no_encontrado': [a['no_encontrado']] if a.get('no_encontrado') else []}
for f in files:
    lote = f.split('/')[-1].replace('.json', '')
    for e in json.load(open(f, encoding='utf-8')):
        i = int(e['ID'])
        upd = dict(e.get('updates', {}))
        for k in list(upd):
            if k == 'URL del documento':   # constant column; route URL to sources instead
                extra_sources.setdefault(i, []).append(upd.pop(k))
        upd.update(OVERRIDES.get(i, {}))
        for h, v in upd.items():
            if h in NEVER_TOUCH:
                continue
            assert h in hdr, (f, i, h)
            v = clean(h, v)
            if h in NUMERIC and v is not None and not isinstance(v, (int, float)):
                raise ValueError(f'non-numeric {f} {i} {h} {v!r}')
            cell = ws.cell(row_of[i], hdr[h])
            old = cell.value
            if old == v or (isinstance(old, float) and isinstance(v, (int, float)) and abs(old - v) < 1e-9):
                continue
            cell.value = v
            cell.fill = FILL_ALTA if i in alta_ids else FILL
            if h in numfmt and isinstance(v, (int, float)):
                cell.number_format = numfmt[h]
            changes.append((i, h, old, v))
        srcs = [s for s in e.get('fuentes_nuevas', []) if s] + extra_sources.get(i, [])
        if srcs:
            extra_sources[i] = srcs
        n = notes.setdefault(i, {'lote': [], 'verificacion': [], 'no_encontrado': []})
        n['lote'].append(lote)
        if e.get('verificacion'):
            n['verificacion'].append(e['verificacion'])
        if e.get('no_encontrado'):
            n['no_encontrado'].append(e['no_encontrado'])

# sources: append new URLs to 'Fuentes de la ficha'
zc = hdr['Fuentes de la ficha']
for i, srcs in extra_sources.items():
    cell = ws.cell(row_of[i], zc)
    cur = cell.value or ''
    have = set(cur.split('\n'))
    add = [s for s in dict.fromkeys(srcs) if s not in have]
    if add:
        old = cell.value
        cell.value = (cur + '\n' if cur else '') + '\n'.join(add)
        cell.fill = FILL_ALTA if i in alta_ids else FILL
        changes.append((i, 'Fuentes de la ficha', old, cell.value))

# stale "límites del juicio" wording where headcount is now filled
uc, agc = hdr['Límites del juicio'], hdr['Personal: personas (ocupadas)']
for i, r in row_of.items():
    cell = ws.cell(r, uc)
    if isinstance(cell.value, str) and U_OLD in cell.value and ws.cell(r, agc).value is not None:
        old = cell.value
        cell.value = old.replace(U_OLD, U_NEW)
        cell.fill = FILL
        changes.append((i, 'Límites del juicio', old, cell.value))
    if i == 43 and isinstance(cell.value, str) and 'No se ha cuantificado plantilla ocupada' in cell.value and ws.cell(r, agc).value:
        old = cell.value
        cell.value = old.replace('No se ha cuantificado plantilla ocupada', 'Plantilla: 17 de 22 puestos RPT cubiertos (jul-2026, ver columnas de personal)')
        cell.fill = FILL
        changes.append((i, 'Límites del juicio', old, cell.value))

# revision date on changed rows
changed_ids = sorted({c[0] for c in changes})
afc = hdr['Fecha de revisión']
for i in changed_ids:
    if i not in alta_ids:          # altas keep their own revision date
        ws.cell(row_of[i], afc).value = REV_DATE

name = {i: ws.cell(r, hdr['Nombre']).value for i, r in row_of.items()}

# ---- change log sheet
base_font = copy.copy(ws.cell(2, 5).font)
hdr_font = copy.copy(ws.cell(1, 1).font)
hdr_fill = copy.copy(ws.cell(1, 1).fill)
for title in ('Cambios 12-10-2026', 'Verificación y pendientes'):
    if title in wb.sheetnames:
        del wb[title]
lg = wb.create_sheet('Cambios 12-10-2026')
cols = ['ID', 'Nombre', 'Columna', 'Letra', 'Valor anterior', 'Valor nuevo']
lg.append(cols)
for a in ALTAS:
    lg.append([a['ID'], name[a['ID']], 'Fila nueva (alta del 14/10/2026)', None, None,
               'Ficha completa añadida al inventario (fondo verde en Hoja 1). Fuentes y verificación en «Verificación y pendientes».'])
for i, h, old, new in sorted(changes, key=lambda c: (c[0], hdr[c[1]])):
    lg.append([i, name[i], h, L(hdr[h]), old, new])
for c in range(1, len(cols) + 1):
    lg.cell(1, c).font = hdr_font
    lg.cell(1, c).fill = hdr_fill
for row in lg.iter_rows(min_row=2):
    for cell in row:
        cell.font = base_font
        cell.alignment = Alignment(wrap_text=True, vertical='top')
for c, w in zip('ABCDEF', [6, 40, 34, 7, 50, 60]):
    lg.column_dimensions[c].width = w
lg.freeze_panes = 'A2'
lg.auto_filter.ref = f'A1:F{lg.max_row}'

vp = wb.create_sheet('Verificación y pendientes')
cols2 = ['ID', 'Nombre', 'Comunidad autónoma', 'Celdas cambiadas', 'Cómo se verificó (documento, página, fila, unidad)', 'Qué sigue sin cifra y por qué']
vp.append(cols2)
ccount = {}
for c in changes:
    ccount[c[0]] = ccount.get(c[0], 0) + 1
for i in sorted(notes):
    n = notes[i]
    vp.append([i, name[i], ws.cell(row_of[i], hdr['Comunidad autónoma']).value, ccount.get(i, 0),
               '\n\n'.join(n['verificacion']) or None, '\n\n'.join(n['no_encontrado']) or None])
for c in range(1, len(cols2) + 1):
    vp.cell(1, c).font = hdr_font
    vp.cell(1, c).fill = hdr_fill
for row in vp.iter_rows(min_row=2):
    for cell in row:
        cell.font = base_font
        cell.alignment = Alignment(wrap_text=True, vertical='top')
for c, w in zip('ABCDEF', [6, 40, 16, 10, 90, 70]):
    vp.column_dimensions[c].width = w
vp.freeze_panes = 'A2'
vp.auto_filter.ref = f'A1:F{vp.max_row}'

# ---- summary sheet: keep cuts separate, counts by formula, coverage block
es = wb['Entidades']
H = "'Hoja 1'!"
# formulas of the original summary sheet point at rows 2 to 126; extend them to the last row
for row in es.iter_rows():
    for cell in row:
        if isinstance(cell.value, str) and cell.value.startswith('='):
            cell.value = re.sub(r'(\$?[A-Z]{1,3}\$?2:\$?[A-Z]{1,3}\$?)%d(?![0-9])' % (N_ORIG + 1), lambda m: m.group(1) + str(LAST), cell.value)
from collections import Counter as _C
_amb = _C(ws.cell(r, hdr['Ámbito']).value for r in range(2, LAST + 1))
_txt = {'Estatal': 'estatales', 'Estatal: creación legal no confirmada operativa': 'creaciones legales de constitución no confirmada',
        'Estatal: creación anunciada o en tramitación, no constituida': 'creaciones anunciadas o en tramitación, no constituidas',
        'Autonómico': 'autonómicos'}
assert set(_amb) <= set(_txt), set(_amb) - set(_txt)
es['A2'] = (f'{N} registros: ' + ' + '.join(f'{_amb[k]} {v}' for k, v in _txt.items() if _amb[k]) +
            '. Creados o transformados desde 2004. Inventario parcial, no censo exhaustivo.' +
            (f' Las filas {N_ORIG + 2} a {LAST} de Hoja 1 (fondo verde) son altas del 14/10/2026.' if ALTAS else ''))
CUT = 'Hasta 31/08/2026:8 meses, NO año completo'
es['E5'] = f'="Personal 2026 reconocido hasta 31/08 (IGAE), EUR millones ("&COUNTIFS({H}AQ2:AQ{LAST},"<>",{H}AS2:AS{LAST},"{CUT}")&" entidades; NO salarios puros; otros cortes en Hoja 1, no se suman)"'
es['F5'] = f'=SUMIFS({H}AQ2:AQ{LAST},{H}AR2:AR{LAST},2026,{H}AS2:AS{LAST},"{CUT}")'
es['E6'] = f'="Pagos personal 2026 hasta 31/08, EUR millones ("&COUNT({H}BI2:BI{LAST})&" entidades)"'
es['E7'] = f'="Gasto de personal 2025, año completo (cap.1 obligaciones; gastos de personal de cuentas en fundaciones/entes): "&COUNT({H}BP2:BP{LAST})&" entidades, EUR millones; NO sumar con parcial 2026"'
lab_font = copy.copy(es['B5'].font)
es['A9'] = f'Cobertura de campos en Hoja 1 (número de fichas con dato; {N} en total)'
es['A9'].font = copy.copy(es['A4'].font)
cov = [
    ('Presupuesto propio (cualquier año/base)', f'=COUNT({H}K2:K{LAST})'),
    ('Sin presupuesto propio verificado en norma (órganos sin dotación)', f'=COUNTIF({H}O2:O{LAST},"Sin presupuesto propio: órgano*")'),
    ('Extinguidas / suprimidas', f'=COUNTIF({H}O2:O{LAST},"Sin presupuesto propio actual: supresión*")'),
    ('Sin cifra propia actual verificada (pendientes)', f'=COUNTIF({H}O2:O{LAST},"Sin cifra propia actual verificada")'),
    ('Crédito de personal (cap. 1 o gastos de personal)', f'=COUNT({H}AL2:AL{LAST})'),
    ('Gasto de personal ejecutado, columna AQ (año y corte variables; no sumar)', f'=COUNT({H}AQ2:AQ{LAST})'),
    ('Gasto de personal 2025 año completo', f'=COUNT({H}BP2:BP{LAST})'),
    ('Personas ocupadas (fecha variable; no sumar)', f'=COUNT({H}AG2:AG{LAST})'),
    ('Puestos aprobados / presupuestados', f'=COUNT({H}AX2:AX{LAST})'),
]
for k, (lab, fml) in enumerate(cov):
    r = 10 + k
    es.cell(r, 2).value = lab
    es.cell(r, 3).value = fml
    es.cell(r, 2).font = lab_font
    es.cell(r, 3).font = lab_font
es['A20'] = ('Celdas con fondo amarillo en Hoja 1: completadas o corregidas el 12/10/2026. Filas con fondo verde: entidades añadidas el 14/10/2026. '
             'Detalle celda a celda en la hoja "Cambios 12-10-2026"; fuentes, páginas y huecos pendientes en "Verificación y pendientes".')
es['A20'].font = copy.copy(es['A3'].font)
es['A20'].alignment = Alignment(wrap_text=True, vertical='top')
es.merge_cells('A20:F20')
es.row_dimensions[20].height = 45

# per-person personnel cost (formula): gasto de personal 2025 / personas ocupadas
cpp = hdr['Coste de personal por persona 2025 (EUR, calculado)']
BPc, AGc = L(hdr['Gasto personal 2025 reconocido anual (EUR millones)']), L(hdr['Personal: personas (ocupadas)'])
for r in range(2, ws.max_row + 1):
    ws.cell(r, cpp).value = f'=IF(AND(ISNUMBER({BPc}{r}),ISNUMBER({AGc}{r}),{AGc}{r}>0),{BPc}{r}*1000000/{AGc}{r},"")'
    ws.cell(r, cpp).number_format = '#,##0'
CPP = L(cpp)

# classification block (judgement aligned with the P100; see 'Clasificación: motivo', 'base en el P100' and 'destino')
CV_ = L(hdr['Clasificación: veredicto']); CF_ = L(hdr['Clasificación: función']); CU_ = L(hdr['Clasificación: útil / no útil'])
CB_ = L(hdr['Clasificación: base en el P100'])
es['A22'] = f'Clasificación de las {N} fichas según el P100 de Extramuros (juicio con criterios explícitos; motivo, base en el P100 y destino de cada una en Hoja 1)'
es['A22'].font = copy.copy(es['A4'].font)
es['C23'] = 'Fichas'; es['D23'] = 'Con presupuesto propio 2026'; es['E23'] = 'Suma de presupuestos propios 2026, EUR millones (bases distintas: orden de magnitud, no total contable)'
for cc in ('C23', 'D23', 'E23'):
    es[cc].font = copy.copy(es['B5'].font)
    es[cc].alignment = Alignment(wrap_text=True, vertical='top')
labels = [('Útil', CU_), ('No útil', CU_), ('Sin decisión en el P100', CU_), ('Extinguida', CU_),
          ('Mantener', CV_), ('Reformar', CV_), ('Integrar', CV_), ('Suprimir', CV_), ('Pendiente de decisión', CV_), ('Extinguida', CV_),
          ('Servicio público directo', CF_), ('Regulación o inspección de terceros', CF_), ('Financiación y ayudas', CF_),
          ('Control interno y cumplimiento', CF_), ('Consultivo o participación', CF_), ('Extinguida o no constituida', CF_)]
for k, (lab, col) in enumerate(labels):
    r = 24 + k
    es.cell(r, 1).value = {0: 'Binario', 4: 'Veredicto', 10: 'Función'}.get(k)
    es.cell(r, 2).value = lab
    es.cell(r, 3).value = f'=COUNTIF({H}{col}2:{col}{LAST},B{r})'
    es.cell(r, 4).value = f'=COUNTIFS({H}{col}2:{col}{LAST},B{r},{H}L2:L{LAST},2026,{H}K2:K{LAST},">0")'
    es.cell(r, 5).value = f'=SUMIFS({H}K2:K{LAST},{H}{col}2:{col}{LAST},B{r},{H}L2:L{LAST},2026)'
    for c in (1, 2, 3, 4, 5):
        es.cell(r, c).font = copy.copy(es['B5'].font)
    es.cell(r, 5).number_format = '#,##0.0'
es['A40'] = 'Base en el P100'; es['A40'].font = copy.copy(es['B5'].font)
for k, (lab, pat) in enumerate([('Explícito: el P100 nombra el organismo o su categoría', 'Explícito*'),
                                ('Aplicando el criterio del P100 (deducción nuestra)', 'Aplicando*'),
                                ('El P100 no trata la materia', 'El P100*')]):
    r = 41 + k
    es.cell(r, 2).value = lab
    es.cell(r, 3).value = f'=COUNTIF({H}{CB_}2:{CB_}{LAST},"{pat}")'
    es.cell(r, 2).font = copy.copy(es['B5'].font); es.cell(r, 3).font = copy.copy(es['B5'].font)
es['A45'] = ('Criterio (alineado con el P100). Útil no es tener un contenido, es a qué sirve ese contenido. Un organismo es útil si cumple las tres condiciones: '
             '1) su función es necesaria y cambia decisiones o mejora un servicio (un informe, un dictamen o un trámite de cumplimiento no cuenta; Costes del Estado 2); '
             '2) nadie más la presta: con un organismo nacional basta, no hacen falta 17 autonómicos iguales (Costes 9, Organización del Estado 5, Impuestos 11 "una sola Agencia Tributaria", Estado 17 "una sola web"); '
             '3) sirve a un fin del P100, no a un fin que el P100 elimina (p. ej. la cooperación al desarrollo autonómica: el P100 limita la cooperación a la humanitaria y a países que colaboren en el control migratorio, Costes 5). '
             'Veredictos: Mantener (cumple las tres), Reformar (se queda, con los cambios que pide el P100), Integrar (la función sigue, el organismo sobra: pasa al organismo nacional o a la consejería indicada en "destino"), '
             'Suprimir (ni la función ni el organismo), Pendiente de decisión (el P100 no trata la materia), Extinguida (ya no existe). '
             'Binario: Útil = Mantener o Reformar; No útil = Integrar o Suprimir (juzga el organismo, no la materia). '
             '"Explícito" = el P100 lo dice; "Aplicando el criterio" = deducción nuestra a partir del P100, a validar. "Exigida por la UE": se puede fusionar o redimensionar, no suprimir. Es un juicio, no un dato.')
es['A45'].font = copy.copy(es['A3'].font)
es['A45'].alignment = Alignment(wrap_text=True, vertical='top')
es.merge_cells('A45:F45')
es.row_dimensions[45].height = 230

# hidden personnel cost of consultative bodies: scenario from the sheet's own data
es['A47'] = 'Coste de personal de los órganos consultivos sin presupuesto propio (ESCENARIO, no dato publicado)'
es['A47'].font = copy.copy(es['A4'].font)
es['B48'] = 'Órganos consultivos o de participación'; es['C48'] = f'=COUNTIF({H}{CF_}2:{CF_}{LAST},"Consultivo o participación")'
es['B49'] = 'Coste de personal por persona: mediana de la hoja (gasto 2025 / personas), EUR'; es['C49'] = f'=MEDIAN({H}{CPP}2:{CPP}{LAST})'
es['B50'] = 'Fichas con las que se calcula la mediana'; es['C50'] = f'=COUNT({H}{CPP}2:{CPP}{LAST})'
for k, n in enumerate([1, 2, 3]):
    r = 51 + k
    es.cell(r, 2).value = f'Si cada órgano ocupa {n} persona{"s" if n > 1 else ""} a tiempo completo: EUR millones al año'
    es.cell(r, 3).value = f'=C48*C49*{n}/1000000'
    es.cell(r, 3).number_format = '#,##0.0'
es['C49'].number_format = '#,##0'
for r in range(48, 54):
    es.cell(r, 2).font = copy.copy(es['B5'].font); es.cell(r, 3).font = copy.copy(es['B5'].font)
es['A54'] = ('Las normas de estos órganos dicen que su coste lo absorbe el ministerio o la consejería (secretaría, unidad técnica, apoyo a reuniones), pero no lo publican por separado. '
             'Las personas a tiempo completo por órgano son un supuesto; el coste por persona sale de la hoja. Casos documentados en la columna "Coste de apoyo" de Hoja 1 (p. ej. 7 personas en el órgano de trabajo del Observatorio de la Vida Militar, 2015). '
             'Suprimir el órgano libera ese coste solo si se amortizan o reasignan los puestos que lo atienden.')
es['A54'].font = copy.copy(es['A3'].font)
es['A54'].alignment = Alignment(wrap_text=True, vertical='top')
es.merge_cells('A54:F54')
es.row_dimensions[54].height = 75

# duplication sheet
import glob as _g
CCs = ['Andalucía', 'Aragón', 'Asturias', 'Illes Balears', 'Canarias', 'Cantabria', 'Castilla-La Mancha', 'Castilla y León',
       'Cataluña', 'Comunitat Valenciana', 'Extremadura', 'Galicia', 'Madrid', 'Murcia', 'Navarra', 'País Vasco', 'La Rioja']
if 'Duplicidades por tema' in wb.sheetnames:
    del wb['Duplicidades por tema']
dsh = wb.create_sheet('Duplicidades por tema', 1)
TIPO = {'ente': 'Propio (ente)', 'organo': 'Propio (órgano)', 'estado': 'Lo cubre el Estado', 'consejeria': 'Consejería',
        'no': 'No existe', 'no_verificado': 'Sin verificar'}
STATE_N = {'Entes de emergencias 112': 0, 'Agencias de ciberseguridad': 2, 'Agencias de investigación e innovación': 2}
head = ['Tema', 'Organismo estatal'] + CCs + ['CCAA con organismo propio', 'CCAA sin verificar', 'Organismos en total (Estado + CCAA, verificados)',
                                            '¿Cubre el Estado esos territorios?', 'Base competencial', 'Fuentes']
dsh.append(head)
temas_all = []
for f in sorted(_g.glob(str(RES / 'DUP*.json'))):
    temas_all += json.load(open(f, encoding='utf-8'))
for t in temas_all:
    r = dsh.max_row + 1
    row = [t['tema'], (t.get('estado') or {}).get('nombre')]
    for k in CCs:
        c = t['ccaa'][k]
        tp = c.get('tipo')
        row.append(f"{TIPO.get(tp, tp)}: {c['nombre']}" if tp in ('ente', 'organo') and c.get('nombre') else TIPO.get(tp, tp))
    row += [None, None, None, t.get('cobertura_estatal'), t.get('competencia'), '\n'.join(t.get('fuentes') or [])]
    dsh.append(row)
    c0, c1 = L(3), L(2 + len(CCs))
    dsh.cell(r, 3 + len(CCs)).value = f'=COUNTIF({c0}{r}:{c1}{r},"Propio*")'
    dsh.cell(r, 4 + len(CCs)).value = f'=COUNTIF({c0}{r}:{c1}{r},"Sin verificar")'
    dsh.cell(r, 5 + len(CCs)).value = f'={STATE_N.get(t["tema"], 1)}+{L(3 + len(CCs))}{r}'
for c in range(1, len(head) + 1):
    dsh.cell(1, c).font = hdr_font; dsh.cell(1, c).fill = hdr_fill
    dsh.cell(1, c).alignment = Alignment(wrap_text=True, vertical='top')
    dsh.column_dimensions[L(c)].width = 30 if c <= 2 else (18 if c <= 2 + len(CCs) else 24)
for row in dsh.iter_rows(min_row=2):
    for cell in row:
        cell.font = base_font
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        v = cell.value
        if isinstance(v, str) and v.startswith('Propio'):
            cell.fill = PatternFill('solid', fgColor='FFF4CCCC')
        elif v in ('Lo cubre el Estado', 'Consejería', 'No existe'):
            cell.fill = PatternFill('solid', fgColor='FFE2EFDA')
        elif v == 'Sin verificar':
            cell.fill = PatternFill('solid', fgColor='FFEDEDED')
dsh.freeze_panes = 'C2'
dsh.auto_filter.ref = f'A1:{L(len(head))}{dsh.max_row}'
r = dsh.max_row + 2
dsh.cell(r, 1).value = ('Rojo: la comunidad tiene organismo propio sobre el tema. Verde: no lo tiene (lo cubre el Estado, lo hace la consejería o no existe). Gris: sin verificar. '
                        '"Organismos en total" suma el estatal y los autonómicos verificados; el máximo posible es 18. Fuentes oficiales por celda en el dashboard y en los JSON de trabajo.')
dsh.cell(r, 1).font = copy.copy(es['A3'].font)
dsh.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top')
dsh.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
dsh.row_dimensions[r].height = 45

# CNMC / CSIC spending sheet
if 'Gasto CNMC y CSIC' in wb.sheetnames:
    del wb['Gasto CNMC y CSIC']
gs = wb.create_sheet('Gasto CNMC y CSIC')
gs.append(['Entidad', 'Capítulo', 'Crédito inicial 2026 (= PGE 2023 prorrogado), EUR millones', 'Crédito actualizado a 31/08/2026, EUR millones', 'A qué se destina', '¿Gasto propio o de paso?'])
for e in json.load(open(RES / 'gasto_csic_cnmc.json', encoding='utf-8')):
    for c in e['capitulos']:
        if c.get('importe_m') is None and c.get('importe_inicial_m') is None:
            continue
        cap = c['capitulo']
        paso = 'De paso a terceros' if (e['ID'] == 24 and (cap.startswith('7') or cap.startswith('4'))) else ('Sin desglosar' if '2 a 9' in cap or '3+4' in cap else 'Propio')
        gs.append([e['entidad'], cap, c.get('importe_inicial_m'), c.get('importe_m'), c.get('destino'), paso])
for c in range(1, 7):
    gs.cell(1, c).font = hdr_font; gs.cell(1, c).fill = hdr_fill; gs.cell(1, c).alignment = Alignment(wrap_text=True, vertical='top')
for row in gs.iter_rows(min_row=2):
    for cell in row:
        cell.font = base_font; cell.alignment = Alignment(wrap_text=True, vertical='top')
    for cell in row[2:4]:
        cell.number_format = '#,##0.000'
for c, w in zip('ABCDEF', [30, 34, 18, 18, 70, 18]):
    gs.column_dimensions[c].width = w
r = gs.max_row + 2
gs.cell(r, 1).value = ('CNMC: el capítulo 7 (y 110 M del capítulo 4, servicio postal universal) es dinero que el Estado le transfiere y ella aplica a costes regulados del sistema eléctrico '
                       '(Ley 15/2012, subastas de CO2 de la Ley 7/2021, sobrecoste extrapeninsular de la Ley 24/2013). Fuente: presupuesto CNMC 2023 en su portal de transparencia e IGAE agosto 2026. '
                       'CSIC: solo está verificado el capítulo 1; el reparto del resto entre capítulos no se pudo leer.')
gs.cell(r, 1).font = copy.copy(es['A3'].font); gs.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top')
gs.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
gs.row_dimensions[r].height = 70

wb.save(out)
print('changes', len(changes), 'rows', len(changed_ids))
