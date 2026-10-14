"""Reproduce the whole analysis from the original sheet and the saved research results.
Works the same on Windows, macOS and Linux. No network access.

Usage (from anywhere):  python scripts/run_all.py
"""
import os
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'salida' / 'Entidades_publicas_poder_y_presupuesto_v6.xlsx'
ENV = {**os.environ, 'PYTHONUTF8': '1'}   # UTF-8 everywhere, also on Windows consoles

STEPS = [
    ('Altas: fichas nuevas a partir de los encargos 28-31', ['preparar_altas.py']),
    ('Clasificación v1 (histórica: niveles A-D)', ['clasificacion.py']),
    ('Clasificación v2 (función, tema, duplicidad, UE, actividad; datos de duplicidades)', ['clasificacion2.py']),
    ('Clasificación v3 (veredicto alineado con el P100)', ['clasificacion3.py']),
    ('Excel: hoja original + todos los resultados + clasificación', ['apply.py', str(OUT)]),
    ('Datos del dashboard', ['build_dash_data.py', str(OUT)]),
    ('Páginas del dashboard (index.html y preview.html)', ['build_dashboard.py']),
    ('CSV de la clasificación', ['export_csv.py', str(OUT)]),
    ('Comprobaciones', ['validate_dashboard_data.py']),
]

for i, (label, cmd) in enumerate(STEPS, 1):
    print(f'[{i}/{len(STEPS)}] {label}', flush=True)
    r = subprocess.run([sys.executable, str(BASE / 'scripts' / cmd[0]), *cmd[1:]], cwd=BASE, env=ENV)
    if r.returncode:
        sys.exit(f'Falló el paso {i} ({label}).')

print(f'Hecho: {OUT.relative_to(BASE)}, dashboard/index.html y dashboard/preview.html.')
print('Las fórmulas del Excel se calculan al abrirlo en Excel, LibreOffice o Google Sheets.')
