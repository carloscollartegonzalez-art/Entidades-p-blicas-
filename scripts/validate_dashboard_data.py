"""Validate dashboard JSON datasets and calcs.js input wiring.

Usage (from repo root): python scripts/validate_dashboard_data.py
"""
import json
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'scripts'))
from inventario import ids_inventario
N_ESPERADO = len(ids_inventario())
D = BASE / 'dashboard'
ENC = 'utf-8'

DATASETS = [
    'entidades', 'referencias_matriz', 'personal_desglose', 'csic_personal', 'verificacion_muestra',
    'gasto_capitulos', 'duplicidades', 'temas',
]

CALC_RE = re.compile(r"dash\.calc\(\s*'([^']+)'\s*,\s*\{[^}]*inputs:\s*\[([^\]]*)\]", re.MULTILINE)


def main() -> int:
    errors: list[str] = []

    for name in DATASETS:
        path = D / 'datos' / f'{name}.json'
        if not path.is_file():
            errors.append(f'missing dataset file: {path.relative_to(BASE)}')
            continue
        try:
            data = json.loads(path.read_text(encoding=ENC))
        except json.JSONDecodeError as exc:
            errors.append(f'invalid JSON in {path.name}: {exc}')
            continue
        if not isinstance(data, list):
            errors.append(f'{path.name}: root must be a JSON array')
        elif name == 'entidades' and len(data) != N_ESPERADO:
            errors.append(f'entidades.json: expected {N_ESPERADO} rows (original sheet + altas), got {len(data)}')

    # Guard against a workbook rebuilt without the research results (apply.py with a subset of files):
    # the dashboard must have more budgets than the original sheet and a non-empty staff breakdown.
    try:
        import openpyxl
        ent = json.loads((D / 'datos' / 'entidades.json').read_text(encoding=ENC))
        des = json.loads((D / 'datos' / 'personal_desglose.json').read_text(encoding=ENC))
        ws = openpyxl.load_workbook(BASE / 'datos' / 'entrada' / 'Entidades_publicas_poder_y_presupuesto_final_125.xlsx',
                                    read_only=True)['Hoja 1']
        rows = list(ws.iter_rows(values_only=True))
        col = rows[0].index('Presupuesto propio (EUR millones)')
        n_orig = sum(1 for r in rows[1:] if isinstance(r[col], (int, float)))
        n_dash = sum(1 for e in ent if e.get('presupuesto_m') is not None)
        if n_dash <= n_orig:
            errors.append(f'entidades.json tiene {n_dash} presupuestos, no más que la hoja original ({n_orig}): '
                          'el Excel se generó sin los resultados de la investigación. Ejecuta python scripts/run_all.py')
        if not des:
            errors.append('personal_desglose.json está vacío: el Excel se generó sin los resultados de personal (P1-P6). '
                          'Ejecuta python scripts/run_all.py')
    except Exception as exc:  # pragma: no cover
        errors.append(f'no se pudo comprobar la cobertura de datos: {exc}')

    calcs = (D / 'calcs.js').read_text(encoding=ENC)
    calc_defs = CALC_RE.findall(calcs)
    calc_ids = {cid for cid, _ in calc_defs}
    allowed_inputs = set(DATASETS) | calc_ids
    for calc_id, inputs_raw in calc_defs:
        for inp in re.findall(r"'([^']+)'", inputs_raw):
            if inp not in allowed_inputs:
                errors.append(f"calcs.js: dash.calc('{calc_id}') references unknown input '{inp}'")

    preview = D / 'preview.html'
    if preview.is_file():
        text = preview.read_text(encoding=ENC)
        if 'cdnjs.cloudflare.com/ajax/libs/d3' in text:
            errors.append('preview.html still references cdnjs d3 — run scripts/build_dashboard.py')
        if 'vendor/d3.min.js' not in text:
            errors.append('preview.html missing vendor/d3.min.js script tag')

    index = D / 'index.html'
    app_src = (D / 'app.js').read_text(encoding=ENC)
    if index.is_file() and 'hashchange' not in app_src:
        errors.append('app.js missing hashchange handler (index.html may be stale)')

    if errors:
        print('validate_dashboard_data: FAILED')
        for e in errors:
            print(' -', e)
        return 1

    print('validate_dashboard_data: OK')
    print(f'  datasets: {len(DATASETS)} files')
    print(f'  dash.calc definitions: {len(calc_ids)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
