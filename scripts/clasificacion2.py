"""Second classification (after user feedback): function type + duplication + verdict.
Rule: Extinguida -> Extinguida; Consultivo -> Prescindible; Control/cumplimiento duplicado -> Prescindible;
Control/cumplimiento -> Revisable; sustantiva que duplica a un organismo estatal que ya cubre el territorio -> Revisable;
en arranque sin actividad -> Revisable; resto -> Útil.
Writes datos/resultados/Z_clasificacion_v2.json and dashboard/datos/temas.json, dashboard/datos/duplicidades.json."""
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent  # raíz del repositorio
RES = BASE / 'datos' / 'resultados'
DASH = BASE / 'dashboard' / 'datos'
import json, glob
from collections import Counter

old = {e['ID']: e['updates'] for e in json.load(open(RES / 'Z_clasificacion_v1.json', encoding='utf-8'))}
CC = ['Andalucía', 'Aragón', 'Asturias', 'Illes Balears', 'Canarias', 'Cantabria', 'Castilla-La Mancha', 'Castilla y León',
      'Cataluña', 'Comunitat Valenciana', 'Extremadura', 'Galicia', 'Madrid', 'Murcia', 'Navarra', 'País Vasco', 'La Rioja']
temas = []
for f in sorted(glob.glob(str(RES / 'DUP*.json'))):
    temas += json.load(open(f, encoding='utf-8'))
T = {t['tema']: t for t in temas}
STATE_N = {'Entes de emergencias 112': 0, 'Agencias de ciberseguridad': 2, 'Agencias de investigación e innovación': 2}
ESTADO_CORTO = {
    'Agencias tributarias': 'AEAT', 'Consejos de transparencia': 'CTBG', 'Autoridades de protección de datos': 'AEPD',
    'Autoridades de defensa de la competencia': 'CNMC',
    'Oficinas y agencias antifraude y de protección del informante': 'AIPI', 'Agencias de calidad universitaria': 'ANECA',
    'Evaluación de políticas públicas': 'Agencia Estatal de Evaluación', 'Escuelas e institutos de formación de empleados públicos': 'INAP',
    'Agencias de ciberseguridad': 'INCIBE y CCN-CERT', 'Agencias de administración digital y TIC': 'AEAD',
    'Agencias de investigación e innovación': 'AEI y CDTI', 'Agencias de la energía': 'IDAE', 'Seguridad ferroviaria': 'AESF',
    'Agencias de salud pública': 'AESAP', 'Agencias de cooperación al desarrollo': 'AECID',
    'Institutos de seguridad y salud laboral': 'INSST', 'Entes de emergencias 112': 'DG de Protección Civil (no es agencia)',
    'Observatorios de convivencia escolar': 'Observatorio Estatal', 'Consejos de la juventud': 'Consejo de la Juventud de España',
    'Observatorios de igualdad y violencia de género': 'Observatorio Estatal de Violencia sobre la Mujer',
    'Consejos audiovisuales (reguladores)': 'CNMC'}
# coverage: does the state body already cover the territory of an autonomic copy? (from each topic's cobertura_estatal)
CUBRE = {'Consejos de transparencia', 'Autoridades de protección de datos', 'Autoridades de defensa de la competencia',
         'Agencias de calidad universitaria', 'Agencias de ciberseguridad'}

conteo = {}
for t in temas:
    c = Counter(t['ccaa'][k].get('tipo') for k in CC)
    sn = STATE_N.get(t['tema'], 1)
    conteo[t['tema']] = dict(estado=sn, ente=c['ente'], organo=c['organo'], cubre_estado=c['estado'],
                             consejeria=c['consejeria'], no=c['no'], no_verificado=c['no_verificado'],
                             total=sn + c['ente'] + c['organo'])

TR, TP, DA, CO, AF, UN, EV, FO, CI, TI, ID, EN, FE, SA, COO, LA, E112, CV, JU, IG, AV = (
    'Agencias tributarias', 'Consejos de transparencia', 'Autoridades de protección de datos',
    'Autoridades de defensa de la competencia', 'Oficinas y agencias antifraude y de protección del informante',
    'Agencias de calidad universitaria', 'Evaluación de políticas públicas',
    'Escuelas e institutos de formación de empleados públicos', 'Agencias de ciberseguridad',
    'Agencias de administración digital y TIC', 'Agencias de investigación e innovación', 'Agencias de la energía',
    'Seguridad ferroviaria', 'Agencias de salud pública', 'Agencias de cooperación al desarrollo',
    'Institutos de seguridad y salud laboral', 'Entes de emergencias 112', 'Observatorios de convivencia escolar',
    'Consejos de la juventud', 'Observatorios de igualdad y violencia de género', 'Consejos audiovisuales (reguladores)')
for k in [TR, TP, DA, CO, AF, UN, EV, FO, CI, TI, ID, EN, FE, SA, COO, LA, E112, CV, JU, IG, AV]:
    assert k in T, k

S, R, F, K, C, X = ('Servicio público directo', 'Regulación o inspección de terceros', 'Financiación y ayudas',
                    'Control interno y cumplimiento', 'Consultivo o participación', 'Extinguida o no constituida')
UE = {
    2: 'Sí: el Reglamento (UE) 2018/1139 exige una autoridad nacional de aviación civil',
    5: 'Sí: la Directiva 2011/85/UE exige un organismo fiscal independiente',
    7: 'Sí: la Directiva (UE) 2016/798 exige una autoridad nacional de seguridad ferroviaria',
    24: 'Sí: las directivas de energía y comunicaciones exigen un regulador nacional independiente',
    28: 'Sí: la Directiva (UE) 2019/633 exige una autoridad de control de prácticas comerciales desleales',
    35: 'Sí: la normativa farmacéutica de la UE exige una autoridad nacional competente',
    39: 'Sí: el Reglamento (UE) 2021/817 exige una agencia nacional de Erasmus+',
    41: 'Sí: el Reglamento (UE) 2024/1689 exige una autoridad de vigilancia del mercado de IA',
    43: 'Sí: la Directiva (UE) 2019/1937 exige autoridades de canal externo de denuncias',
    44: 'Sí: las directivas de igualdad de trato exigen un organismo de igualdad',
}
# ID: (function, tema, duplication kind or None, override verdict or None)
M = {
 1: (X, EV, None, None), 2: (R, 'Seguridad aérea', None, None), 3: (R, 'Antidopaje', None, None),
 4: (F, ID, 'estatal', None), 5: (K, 'Supervisión fiscal', None, None), 6: (K, TP, 'estatal', None),
 7: (R, FE, 'estatal', None), 8: (C, CV, 'estatal', None), 9: (C, 'Vida militar', None, None),
 10: (C, 'Becas universitarias', None, None), 11: (C, 'Empleo público', None, None),
 12: (C, 'Internacionalización empresarial', None, None), 13: (C, IG, 'estatal', None),
 14: (S, 'Violencia de género (política estatal)', None, None), 15: (C, 'Familias', None, None),
 16: (C, 'Discapacidad', None, None), 17: (C, 'Libro y lectura', None, None), 18: (C, 'Nutrición y obesidad', None, None),
 19: (C, 'Responsabilidad social empresarial', None, None), 20: (C, 'Participación: pueblo gitano', None, None),
 21: (C, 'Participación: mujeres', None, None), 22: (F, 'Libertad religiosa', None, None),
 23: (K, 'Supervisión de la contratación pública', None, None), 24: (R, CO, 'estatal', None),
 25: (X, CO, None, None), 26: (X, 'Sector postal', None, None), 27: (X, 'Seguridad alimentaria y consumo', None, None),
 28: (R, 'Cadena alimentaria', None, None), 29: (C, 'Cadena alimentaria', None, None),
 30: (R, 'Inspección de trabajo', None, None), 31: (F, COO, 'estatal', None), 32: (S, 'Diario oficial', None, None),
 33: (S, 'Investigación científica', None, None), 34: (S, 'Meteorología', None, None), 35: (R, 'Medicamentos', None, None),
 36: (S, 'Vivienda e infraestructura de Defensa', None, None), 37: (R, 'Agua (cuencas hidrográficas)', None, None),
 38: (R, 'Agua (cuencas hidrográficas)', None, None), 39: (F, 'Programas educativos europeos', None, None),
 40: (F, 'Espacio', None, None), 41: (R, 'Inteligencia artificial', None, None), 42: (S, TI, 'estatal', None),
 43: (K, AF, 'estatal', None), 44: (K, 'Igualdad de trato y no discriminación', None, 'arranque'),
 45: (K, EV, 'estatal', None), 46: (S, SA, 'estatal', 'arranque'), 47: (C, 'Comercio', None, None),
 48: (C, 'Igualdad (sectorial)', None, None), 49: (C, 'Fraude a la Seguridad Social', None, None),
 50: (C, 'Igualdad (sectorial)', None, None), 51: (C, 'Lengua española', None, None), 52: (C, 'Regadío', None, None),
 53: (C, 'Regadío', None, None), 54: (C, 'Morosidad', None, None), 55: (C, 'Márgenes empresariales', None, None),
 56: (C, 'Fraude sanitario', None, None), 57: (C, 'Ética de la Guardia Civil', None, None),
 58: (C, 'Gobierno abierto', None, None), 59: (C, 'Digitalización agroalimentaria', None, None),
 60: (C, 'Derechos digitales', None, None), 61: (C, 'Agenda 2030', None, None),
 62: (C, 'Participación: personas LGTBI', None, None), 63: (C, 'Participación: infancia', None, None),
 64: (C, 'Seguridad aeroespacial', None, None), 65: (S, 'Patrimonio fotográfico', None, None),
 66: (F, 'Fondos tecnológicos (PERTE)', None, None), 67: (C, 'Desertificación', None, None),
 68: (C, 'Eclipses 2026-2028', None, None), 69: (C, 'Riesgo de desastres', None, None),
 70: (X, AV, None, None), 71: (X, 'Juego', None, None), 72: (X, 'Tarifas aeroportuarias', None, None),
 73: (F, COO, 'paralelo', None), 74: (R, CO, 'cubre', None), 75: (S, TR, 'propio', None), 76: (K, TP, 'cubre', None),
 77: (C, 'Territorio', None, None), 78: (K, UN, 'cubre', None), 79: (S, E112, 'propio', None), 80: (S, TR, 'propio', None),
 81: (S, TR, 'propio', None), 82: (S, 'Servicios sociales', None, None), 83: (S, LA, 'paralelo', None),
 84: (X, 'Agua (autonómica)', None, None), 85: (C, CV, 'paralelo', None), 86: (S, TR, 'propio', None),
 87: (K, AF, 'paralelo', None), 88: (C, CV, 'paralelo', None), 89: (F, ID, 'paralelo', None), 90: (X, JU, None, None),
 91: (F, 'Turismo', None, None), 92: (K, AF, 'paralelo', None), 93: (R, CO, 'cubre', None), 94: (X, 'Juventud', None, None),
 95: (K, AF, 'paralelo', None), 96: (S, 'Discapacidad: apoyo jurídico', None, None), 97: (S, TI, 'propio', None),
 98: (F, 'Desarrollo empresarial', None, None), 99: (K, UN, 'cubre', None), 100: (S, SA, 'paralelo', 'arranque'),
 101: (S, E112, 'propio', None), 102: (X, 'Espacios naturales', None, None), 103: (R, 'Disciplina urbanística', None, None),
 104: (R, FE, 'propio_red', None), 105: (X, 'Residuos', None, None), 106: (S, 'Radiotelevisión pública', None, None),
 107: (S, 'Reinserción social', None, None), 108: (S, CI, 'cubre', None), 109: (S, 'Puertos deportivos', None, None),
 110: (S, CI, 'cubre', None), 111: (S, SA, 'paralelo', 'arranque'), 112: (F, ID, 'paralelo', None),
 113: (K, TP, 'cubre', None), 114: (S, E112, 'propio', None), 115: (C, JU, 'paralelo', None), 116: (S, FO, 'propio', None),
 117: (F, ID, 'paralelo', None), 118: (S, TI, 'propio', None), 119: (X, EN, None, None), 120: (S, TI, 'propio', 'arranque'),
 121: (R, 'Calidad alimentaria', None, None), 122: (F, EN, 'paralelo', None), 123: (C, IG, 'paralelo', None),
 124: (S, TI, 'propio', None), 125: (F, EN, 'paralelo', None),
}
assert sorted(M) == list(range(1, 126))


def dup_text(i, tema, kind):
    if tema not in conteo:
        return None
    n = conteo[tema]
    est = ESTADO_CORTO[tema]
    base = f"{n['total']} organismos sobre este tema entre el Estado y las CCAA (verificados)"
    if kind == 'estatal':
        return f"Organismo estatal de referencia. {n['ente'] + n['organo']} comunidades tienen el suyo propio; {base}."
    if kind == 'cubre':
        return f"Duplica a {est}, que ya cubre este territorio o puede hacerlo. {base}."
    if kind == 'paralelo':
        return f"Paralelo a {est}: cada nivel actúa con sus propios fondos o competencias. {base}."
    if kind == 'propio_red':
        return f"Supervisa una red que {est} no cubre por ley (red autonómica); no es duplicado. {base}."
    if kind == 'propio':
        return f"Competencia autonómica que el Estado no presta en ese territorio; la duplicidad es de forma (agencia propia o dirección general). {base}."
    return base


out = []
cnt = Counter()
for i, (fn, tema, kind, ov) in sorted(M.items()):
    o = old[i]
    prev = o['Clasificación: motivo']
    if fn == X:
        ver, why = 'Extinguida', prev
    elif fn == C:
        ver, why = 'Prescindible', 'Órgano consultivo o de participación sin medios propios. ' + prev
    elif fn == K and kind == 'cubre':
        ver, why = 'Prescindible', f'Función de control o cumplimiento que además duplica a {ESTADO_CORTO[tema]}. ' + prev
    elif fn == K:
        ver, why = 'Revisable', 'Función de control o cumplimiento de la propia administración (no presta un servicio ni regula a terceros). ' + prev
    elif kind == 'cubre':
        ver, why = 'Revisable', f'Función sustantiva, pero duplica a {ESTADO_CORTO[tema]}, que ya cubre este territorio. ' + prev
    elif ov == 'arranque':
        ver, why = 'Revisable', 'Función sustantiva, pero sin actividad ni medios propios acreditados todavía. ' + prev
    else:
        ver, why = 'Útil', prev
    cnt[ver] += 1
    binario = {'Útil': 'Útil', 'Revisable': 'No útil', 'Prescindible': 'No útil', 'Extinguida': 'Extinguida'}[ver]
    n = conteo.get(tema)
    out.append({'ID': i, 'updates': {
        'Clasificación: útil / no útil': binario,
        'Clasificación: veredicto': ver,
        'Clasificación: función': fn,
        'Clasificación: duplicidad': dup_text(i, tema, kind),
        'Clasificación: exigida por la UE': UE.get(i, 'No'),
        'Clasificación: actividad reciente': o['Clasificación: actividad reciente'],
        'Clasificación: motivo': why,
        'Tema funcional': tema,
        'Organismos del mismo tema (Estado + CCAA, verificados)': n['total'] if n else None,
    }})

# support of consultative bodies
ap = {e['ID']: e for e in json.load(open(RES / 'C_apoyo.json', encoding='utf-8'))}
for e in out:
    a = ap.get(e['ID'])
    if not a:
        continue
    parts = []
    if a.get('unidad_apoyo'): parts.append('Apoyo: ' + a['unidad_apoyo'].rstrip('.'))
    if a.get('puestos_asignados') is not None: parts.append(f"puestos asignados según fuente oficial: {a['puestos_asignados']}")
    if a.get('vocales') is not None: parts.append(f"vocales: {a['vocales']}")
    if a.get('retribucion_miembros'): parts.append('miembros: ' + a['retribucion_miembros'])
    if a.get('gasto_identificable'): parts.append('gasto con nombre propio: ' + str(a['gasto_identificable']))
    e['updates']['Coste de apoyo (sin presupuesto propio): unidad, vocales y dietas'] = '. '.join(parts) + '.'
    if a.get('fuente', '').startswith('https://'):
        e['fuentes_nuevas'] = [a['fuente']]

json.dump(out, open(RES / 'Z_clasificacion_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(cnt)

# dashboard datasets for duplication
ABBR = {'Andalucía': 'AND', 'Aragón': 'ARA', 'Asturias': 'AST', 'Illes Balears': 'BAL', 'Canarias': 'CAN', 'Cantabria': 'CNT',
        'Castilla-La Mancha': 'CLM', 'Castilla y León': 'CYL', 'Cataluña': 'CAT', 'Comunitat Valenciana': 'VAL',
        'Extremadura': 'EXT', 'Galicia': 'GAL', 'Madrid': 'MAD', 'Murcia': 'MUR', 'Navarra': 'NAV', 'País Vasco': 'PV', 'La Rioja': 'RIO'}
TIPO_TXT = {'ente': 'Organismo propio con personalidad', 'organo': 'Órgano propio sin personalidad', 'estado': 'Lo cubre el organismo estatal',
            'consejeria': 'Lo hace la consejería', 'no': 'No existe', 'no_verificado': 'Sin verificar'}
dup_rows, tema_rows = [], []
for t in temas:
    st = t.get('estado') or {}
    url = st.get('url') if str(st.get('url', '')).startswith('https://') else None
    dup_rows.append({'clave': f"{t['tema']}|Estado", 'tema': t['tema'], 'territorio': 'Estado', 'abrev': 'EST',
                     'tipo': 'estatal' if STATE_N.get(t['tema'], 1) else 'no', 'tipo_texto': 'Organismo estatal' if STATE_N.get(t['tema'], 1) else 'Sin agencia estatal',
                     'nombre': st.get('nombre'), 'nota': None, 'url': url})
    for k in CC:
        c = t['ccaa'][k]
        u = c.get('url') if str(c.get('url', '')).startswith('https://') else None
        dup_rows.append({'clave': f"{t['tema']}|{k}", 'tema': t['tema'], 'territorio': k, 'abrev': ABBR[k], 'tipo': c.get('tipo'),
                         'tipo_texto': TIPO_TXT.get(c.get('tipo'), c.get('tipo')), 'nombre': c.get('nombre'),
                         'nota': (c.get('nota') or '')[:300] or None, 'url': u})
    n = conteo[t['tema']]
    tema_rows.append({'tema': t['tema'], 'organismo_estatal': ESTADO_CORTO[t['tema']],
                      'competencia': (t.get('competencia') or '')[:400], 'cobertura_estatal': (t.get('cobertura_estatal') or '')[:400],
                      'cubre_estado': t['tema'] in CUBRE})
json.dump(dup_rows, open(DASH / 'duplicidades.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(tema_rows, open(DASH / 'temas.json', 'w', encoding='utf-8'), ensure_ascii=False)
for t, n in sorted(conteo.items(), key=lambda x: -x[1]['total']):
    print(f"{n['total']:>3} (+{n['no_verificado']} sin verificar)  {t}")
