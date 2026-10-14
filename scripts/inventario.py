"""Qué fichas forman el inventario: las de la hoja original más las altas posteriores.

Lo usan las clasificaciones, apply.py y la comprobación final para no depender de un número fijo de filas.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HOJA_ORIGINAL = BASE / 'datos' / 'entrada' / 'Entidades_publicas_poder_y_presupuesto_final_125.xlsx'
# Altas, en el orden en que se añadieron. Cada fichero lo genera scripts/preparar_altas.py.
ALTAS = [BASE / 'datos' / 'entrada' / 'altas_2026-10-14.json']


def ids_hoja_original():
    import openpyxl
    ws = openpyxl.load_workbook(HOJA_ORIGINAL, read_only=True)['Hoja 1']
    return [int(float(r[0])) for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None]


def altas():
    """Lista de altas (dicts con ID, fila, verificacion, no_encontrado), en orden."""
    out = []
    for f in ALTAS:
        out += json.load(open(f, encoding='utf-8'))
    return out


def ids_inventario():
    ids = ids_hoja_original() + [a['ID'] for a in altas()]
    assert len(ids) == len(set(ids)), 'IDs repetidos entre la hoja original y las altas'
    return sorted(ids)
