"""Nombres completos para la columna «destino / matriz de integración» del dashboard."""

# Claves = texto exacto guardado en clasificación; valores = texto para el usuario no experto.
DESTINO_COMPLETO = {
    'CDTI': 'Centro para el Desarrollo Tecnológico y la Innovación (CDTI, E.P.E.)',
    'AEI y CDTI (y la consejería para fondos propios)': (
        'Agencia Estatal de Investigación (AEI) y Centro para el Desarrollo Tecnológico '
        'y la Innovación (CDTI, E.P.E.); la consejería autonómica para fondos propios'
    ),
    'Consejería e instrumentos estatales (ICO, ENISA, CDTI)': (
        'Consejería competente e instrumentos estatales (ICO, ENISA y CDTI, E.P.E.)'
    ),
    'Agencia Tributaria (AEAT)': 'Agencia Estatal de Administración Tributaria (AEAT)',
    'Agencia Estatal de Administración Digital y web única del Estado': (
        'Agencia Estatal de Administración Digital (AEAD) y web única del Estado'
    ),
    'CNMC': 'Comisión Nacional de los Mercados y la Competencia (CNMC)',
    'ANECA': 'Agencia Nacional de Evaluación de la Calidad y Acreditación (ANECA)',
    'CCN-CERT e INCIBE': (
        'Centro Criptológico Nacional (CCN-CERT) e Instituto Nacional de Ciberseguridad (INCIBE)'
    ),
    'AESF': 'Agencia Estatal de Seguridad Ferroviaria (AESF)',
    'AIReF': 'Autoridad Independiente de Responsabilidad Fiscal (AIReF)',
    'Defensor del Pueblo': 'Defensor del Pueblo',
    'Consejo de Transparencia estatal': 'Consejo de Transparencia y Buen Gobierno (CTBG)',
    'Consejo de Transparencia estatal y AEPD': (
        'Consejo de Transparencia y Buen Gobierno (CTBG) y Agencia Española de Protección de Datos (AEPD)'
    ),
    'IDAE (y la consejería)': 'Instituto para la Diversificación y Ahorro de la Energía (IDAE) y la consejería',
    'Instituciones Penitenciarias (Estado)': 'Secretaría General de Instituciones Penitenciarias (Estado)',
    'Consejería': 'Consejería autonómica competente',
    'Consejería (con el INSST como referencia técnica)': (
        'Consejería autonómica competente (con el Instituto Nacional de Seguridad '
        'y Salud en el Trabajo, INSST, como referencia técnica)'
    ),
    'Consejería de salud': 'Consejería de Sanidad de la comunidad autónoma',
    'Consejería de turismo': 'Consejería de Turismo de la comunidad autónoma',
    'Cámara o Sindicatura de Cuentas y, para el canal de denuncias, la AIPI por convenio': (
        'Cámara o Sindicatura de Cuentas de la comunidad autónoma; para denuncias, '
        'Autoridad Independiente de Protección del Informante (AIPI) por convenio'
    ),
    'Estructura ordinaria del ministerio, si alguna función es imprescindible': (
        'Estructura ordinaria del ministerio, si alguna función resultara imprescindible'
    ),
    'Con el criterio de Costes 9, el Ministerio de Sanidad': (
        'Ministerio de Sanidad (criterio Costes del Estado 9)'
    ),
}


def destino_para_mostrar(texto):
    if not texto:
        return texto
    t = texto.strip()
    return DESTINO_COMPLETO.get(t, t)
