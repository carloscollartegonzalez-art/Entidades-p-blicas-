"""Prepara las altas del 14/10/2026: 10 observatorios estatales que faltaban en el inventario.

Lee lo que devolvieron los encargos 28-30 (datos/resultados/AL1-3.json), aplica las correcciones del
verificador independiente (encargo 31, datos/resultados/verificacion_altas.json) y las de método
(solo fuentes oficiales, sin prensa) y escribe:
  - datos/entrada/altas_2026-10-14.json: una ficha completa por alta, con las 73 columnas de la hoja;
  - datos/resultados/C_apoyo_altas.json: unidad de apoyo, vocales y dietas, como C_apoyo.json.
Cada corrección dice de dónde sale. apply.py añade estas filas al final de la Hoja 1.

Uso: python scripts/preparar_altas.py
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RES = BASE / 'datos' / 'resultados'
HEADERS = json.load(open(BASE / 'investigacion' / 'headers.json', encoding='utf-8'))
URL_DOC = 'https://files.instinct.com/q91pr53q4umo-entidades-publicas-poder-y-presupuesto'  # constante de la hoja
FECHA_REV = '14/10/2026'
NO_CONSTITUIDO = 'Estatal: creación anunciada o en tramitación, no constituida'

# ID nuevo por candidato, en orden de fecha del acto que los trae al inventario
IDS = {
    'Observatorio Nacional de Seguridad Vial (DGT)': 126,
    'Observatorio Militar para la Igualdad entre Mujeres y Hombres en las Fuerzas Armadas': 127,
    'Observatorio Permanente del Mercado de los Servicios Portuarios': 128,
    'Observatorio de Igualdad de la Corporación RTVE': 129,
    'Observatorio de Salud de las Mujeres (Ministerio de Sanidad)': 130,
    'Observatorio de Buenas Prácticas Regulatorias': 131,
    'Observatorio de Salud y Cambio Climático (OSCC)': 132,
    'Observatorio de la Vivienda Turística': 133,
    'Observatorio Estatal de la Incapacidad Temporal': 134,
    'Observatorio para la Prevención del Tabaquismo': 135,
}

# Correcciones. Valor str = sustituye la celda; tupla (viejo, nuevo) = sustituye ese texto dentro de la celda
# (falla si no lo encuentra); ('+fuentes', [...]) / ('-fuentes', [...]) = añade o quita URL de «Fuentes de la ficha».
V = 'verificador (encargo 31)'
CORR = {
    126: {  # V: sin correcciones; se añade la URL ELI que usó el verificador
        '+fuentes': ['https://www.boe.es/eli/es/rd/2004/07/02/1599'],
    },
    127: {  # V: la fecha es la del Acuerdo del CM (04/03/2005), no la de las órdenes que lo publican; norma principal Orden DEF/524/2005
        'Fecha legal': '2005-03-04',
        'Norma fundacional': ('Acuerdo del Consejo de Ministros de 04/03/2005, publicado por Orden DEF/524/2005, de 7 de marzo (BOE-A-2005-3769), '
                              'anexo I.1: «Se crea el Centro de estudio sobre la situación de la mujer en las Fuerzas Armadas (Observatorio de la Mujer en las FAS)»; '
                              'también Orden PRE/525/2005, de 7 de marzo (apartado 1.6.a: «Se crea el Observatorio de la Mujer en las Fuerzas Armadas»); '
                              'OM 51/2011, de 28 de julio (nombre actual); Orden DEF/111/2019, de 8 de febrero (BOE núm. 35, de 09/02/2019)'),
        'Límites del juicio': ('La OM 51/2011 (BOD) no se ha leído. Plantilla de la Secretaría Permanente de Igualdad no publicada. '
                               'La identidad entre el «Centro de estudio» citado en el preámbulo de 2019 y el Observatorio de 2005 la confirma la Orden DEF/524/2005 (anexo I.1).'),
        '+fuentes': ['https://www.boe.es/boe/dias/2005/03/08/pdfs/A08109-08110.pdf'],
        'no_encontrado': 'Texto de la OM 51/2011 (BOD); efectivos de la Secretaría Permanente de Igualdad.',
    },
    128: {  # V: el RDLeg 2/2011 solo refunde; la creación legal es la Ley 48/2003 (antes del corte). Entra por su constitución efectiva en 2012.
        'Periodo presidencial': 'Rajoy',
        'Tipo de creación / transformación': ('Constitución efectiva el 29/06/2012 (Rajoy) de un observatorio creado por la Ley 48/2003, de 26 de noviembre, anterior al corte de 2004; '
                                              'regulación vigente en el art. 123 del TRLPEMM (RDLeg 2/2011, texto refundido). La recreación por la Ley 33/2010 no se ha podido verificar'),
        'Fecha legal': '2012-06-29 (constitución efectiva; creación legal 2003-11-26)',
        'Norma fundacional': ('Ley 48/2003, de 26 de noviembre (creación; BOE-A-2003-21615); art. 123 TRLPEMM, RDLeg 2/2011 (refundición; procedencia de la Ley 33/2010 pendiente de verificar); '
                              'acuerdo del Consejo Rector de Puertos del Estado de 29/06/2012 (composición y constitución)'),
        'Límites del juicio': ('Entra en el inventario por su constitución efectiva en 2012: la creación legal (Ley 48/2003) es anterior al 17/04/2004. '
                               'No se ha verificado en texto oficial que el observatorio de 2003 no llegara a constituirse ni que la Ley 33/2010 lo recreara. '
                               'Art. 123 leído en la transcripción de las memorias, no en la página del BOE. Importes de la Oficina Técnica y de los estudios no localizados. '
                               'Recuento de miembros propio a partir de la tabla de vocales.'),
        '+fuentes': ['https://www.boe.es/eli/es/l/2003/11/26/48'],
    },
    129: {  # V: acto de creación no localizado; fecha según intervención parlamentaria. Método: fuera la prensa.
        'Fecha legal': '2018-02 (según intervención parlamentaria)',
        'Estado legal y operativo': ('Creado en febrero de 2018 según el Diario de Sesiones; empezó a funcionar «bastante tiempo más tarde» (DSCG-14-CM-108, p. 4); '
                                     'activo en 2021: en mayo se pidió la comparecencia de su presidenta sobre las memorias de 2018-2020 (DSCG-14-CM-108, p. 3).'),
        'Notas de personal y apoyo ministerial': ('Órgano interno de la Corporación RTVE (sociedad mercantil estatal), no del Ministerio. Composición no verificada en fuente oficial '
                                                  '(según prensa, representantes de los trabajadores, de la dirección y de los sindicatos). Sus resoluciones llevan cabecera de la Secretaría General. '
                                                  'Sin plantilla propia publicada; régimen de retribución o dietas no verificado. No repartir el gasto de la Corporación.'),
        '-fuentes': ['https://www.formulatv.com/noticias/concepcion-cascajosa-convierte-nueva-presidenta--110102/'],
    },
    130: {  # V: fórmula «integración funcional» (preámbulo), adscripción literal y respuesta parlamentaria de 2024
        'Tipo de creación / transformación': ('fue suprimido e integrado en el Observatorio de Salud por la Ley 15/2014',
                                              'quedó integrado funcionalmente en el Observatorio de la Salud por la Ley 15/2014'),
        'Presupuesto: texto completo': ('adscrito al Ministerio de Sanidad a través',
                                        'adscrito al «Ministerio de Sanidad, Consumo y Bienestar Social» (hoy Ministerio de Sanidad) a través'),
        'Estado legal y operativo': ('Recreado 01/03/2019 (La Moncloa anuncia su «regulación y constitución»); según una respuesta parlamentaria del Gobierno de 08/10/2024, '
                                     '«sigue siendo parte de la estructura del Ministerio de Sanidad». Fechas de reunión del Pleno no verificadas.'),
        '+fuentes': ['https://www.congreso.es/entradap/l15p/e4/e_0043016_n_000.pdf'],
    },
    131: {  # V: DA 9.ª verificada en el BOE consolidado de la Ley 20/2013; sustituir la cita de iberley
        'Límites del juicio': ('Texto literal de la DA 9.ª verificado en el BOE consolidado de la Ley 20/2013 (encargo 31). No se ha podido leer en el texto oficial '
                               'si la Ley 18/2022 tiene una cláusula general de no incremento de gasto. No se ha verificado actividad posterior a 2022 (actualizaciones del catálogo, reuniones).'),
        'Fuente legal de consulta normativa': 'https://www.boe.es/eli/es/l/2013/12/09/20/con',
        '+fuentes': ['https://www.boe.es/eli/es/l/2013/12/09/20/con'],
    },
    132: {},  # V: sin correcciones
    133: {  # V: la nota de Mintur no dice qué instrumento aprobó la creación; la de 05/05/2026 no lo menciona
        'Ámbito': NO_CONSTITUIDO,
        'Tipo de creación / transformación': 'Creación anunciada por el Gobierno junto a la Estrategia España Turismo 2030; unidad prevista en la Secretaría de Estado de Turismo',
        'Fecha legal': '2025-10-21 (aprobación anunciada; instrumento no identificado)',
        'Norma fundacional': ('Aprobación anunciada por el Gobierno el 21/10/2025, junto a la Estrategia España Turismo 2030 (nota de prensa del Ministerio de Industria y Turismo; '
                              'instrumento jurídico no identificado); anuncio presidencial 08/10/2025'),
        'Estado legal y operativo': ('Creación anunciada o en tramitación, no constituido: aprobación anunciada por el Gobierno el 21/10/2025; sin instrumento de creación, constitución ni atlas '
                                     'localizados a 14/10/2026. La nota de Mintur de 05/05/2026 sobre la Interministerial de Turismo no lo menciona y dice que «se está trabajando en el desarrollo de un Atlas de Intensidad Turística».'),
        '+fuentes': ['https://www.mintur.gob.es/es-es/gabineteprensa/notasprensa/2026/documents/20260505%20ndp%20interministerial%20de%20turismo%20y%20estrategia%202030.pdf'],
    },
    134: {  # V: sin correcciones; no hay norma publicada
        'Ámbito': NO_CONSTITUIDO,
    },
    135: {  # V: la fecha del CM de 21/07/2026 consta en La Moncloa; método: fuera la prensa jurídica
        'Ámbito': NO_CONSTITUIDO,
        'Límites del juicio': ('Las fechas del Consejo de Ministros (09/09/2025 y 21/07/2026) proceden de prensa jurídica que reproduce la referencia oficial (las notas de Sanidad no se pudieron abrir)',
                               'La fecha del Consejo de Ministros de 21/07/2026 consta en el resumen oficial de La Moncloa; la del anteproyecto (09/09/2025) procede de prensa jurídica (la nota de Sanidad no se pudo abrir)'),
        '+fuentes': ['https://www.lamoncloa.gob.es/consejodeministros/resumenes/paginas/2026/210726-rueda-prensa-ministros.aspx'],
        '-fuentes': ['https://www.laboral-social.com/proyecto-ley-tabaco',
                     'https://www.legaltoday.com/portada-2/portada-2-portada-2/la-aprobacion-en-segunda-vuelta-del-proyecto-de-ley-de-tabaco-amplia-a-las-playas-los-espacios-libres-de-humo-2026-07-21/',
                     'https://www.legaltoday.com/actualidad-juridica/noticias-de-derecho/el-anteproyecto-de-la-ley-del-tabaco-del-gobierno-incluye-por-primera-vez-la-prohibicion-de-fumar-y-vapear-a-menores-2025-09-09/'],
        'no_encontrado': ('Disposición literal de la Ley 15/2014 que lo suprime (el lector del BOE truncó el texto); nota oficial de Sanidad del anteproyecto de 09/09/2025; '
                          'MAIN del proyecto; actividad del órgano entre 2006 y 2014.'),
    },
}

# Apoyo de los órganos sin presupuesto propio (mismo formato que C_apoyo.json; null = la fuente no lo dice)
APOYO_NULO = ('No publicados', 'No fijados ni publicados', 'No consta', 'No regulada', 'No identificado', 'No definidos', 'No aplica', 'No verificada')


def nulo(v):
    # lo que solo dice la prensa tampoco entra (regla 1 del método)
    return None if (v is None or any(str(v).startswith(p) for p in APOYO_NULO) or 'según prensa' in str(v)) else v


def main():
    agentes = {}
    for f in ('AL1', 'AL2', 'AL3'):
        for e in json.load(open(RES / f'{f}.json', encoding='utf-8')):
            agentes[e['candidato']] = (f, e)
    verif = {v['candidato']: v for v in json.load(open(RES / 'verificacion_altas.json', encoding='utf-8'))}
    incluidos = {c for c, (_, e) in agentes.items() if e['incluir']}
    assert incluidos == set(IDS), incluidos ^ set(IDS)

    altas, apoyo = [], []
    for cand, i in sorted(IDS.items(), key=lambda x: x[1]):
        lote, e = agentes[cand]
        fila = {h: e['fila'].get(h) for h in HEADERS}
        extra = set(e['fila']) - set(HEADERS)
        assert not extra, (cand, extra)
        fila['ID'] = i
        fila['URL del documento'] = URL_DOC
        fila['Fecha de revisión'] = FECHA_REV
        c = dict(CORR[i])
        fuentes = [u for u in (fila['Fuentes de la ficha'] or '').split('\n') if u.strip()]
        for u in c.pop('-fuentes', []):
            assert u in fuentes, (i, u)
            fuentes.remove(u)
        for u in c.pop('+fuentes', []):
            if u not in fuentes:
                fuentes.append(u)
        fila['Fuentes de la ficha'] = '\n'.join(fuentes)
        no_enc = c.pop('no_encontrado', e.get('no_encontrado'))
        for h, v in c.items():
            assert h in HEADERS, (i, h)
            if isinstance(v, tuple):
                assert fila[h] and v[0] in fila[h], (i, h, v[0])
                fila[h] = fila[h].replace(v[0], v[1])
            else:
                fila[h] = v
        for malo in ('formulatv', 'laboral-social', 'legaltoday', 'iberley'):
            assert malo not in fila['Fuentes de la ficha'], (i, malo)
        v = verif[cand]
        verificacion = (f"{e.get('verificacion') or ''}\n\nVerificación independiente (encargo 31): norma {v['norma_ok']}, fecha {v['fecha_ok']}, "
                        f"periodo {v['periodo_ok']}, gasto {v['gasto_ok']}, estado {v['estado_ok']}. {v['correcciones']}").strip()
        altas.append({'ID': i, 'lote': lote, 'motivo_inclusion': e['motivo'], 'fila': fila,
                      'verificacion': verificacion, 'no_encontrado': no_enc})
        a = e.get('apoyo') or {}
        if a:
            apoyo.append({'ID': i, 'unidad_apoyo': a.get('unidad_apoyo'), 'puestos_asignados': nulo(a.get('puestos_asignados')),
                          'vocales': nulo(a.get('vocales')), 'retribucion_miembros': nulo(a.get('retribucion_miembros')),
                          'gasto_identificable': nulo(a.get('gasto_identificable')), 'fuente': a.get('fuente')})

    json.dump(altas, open(BASE / 'datos' / 'entrada' / 'altas_2026-10-14.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(apoyo, open(RES / 'C_apoyo_altas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('altas', len(altas), 'apoyo', len(apoyo))


if __name__ == '__main__':
    main()
