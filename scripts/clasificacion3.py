"""Third classification: aligned with Extramuros' P100 (Costes del Estado 2, 3, 5, 9, 10; Organización del Estado 5, 11, 17, 19;
Impuestos 11; Crecer y producir 5, 16; Derogar el sanchismo: Igualdad de Trato) and the user's rule
'útil no es que tenga contenido, sino a qué está sirviendo; si hay una nacional, basta'.
Verdicts: Mantener, Reformar (= útil); Integrar, Suprimir (= no útil); Pendiente de decisión (P100 no lo trata); Extinguida.
Writes datos/resultados/Z_clasificacion.json, keeping función/tema/duplicidad/UE/actividad/coste de apoyo from the v2 file."""
from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent.parent  # raíz del repositorio
RES = BASE / 'datos' / 'resultados'
sys.path.insert(0, str(BASE / 'scripts'))
from destino_labels import destino_para_mostrar
from inventario import ids_inventario

prev = {e['ID']: e for e in json.load(open(RES / 'Z_clasificacion_v2.json', encoding='utf-8'))}
EXP, INF = 'Explícito en el P100', 'Aplicando el criterio del P100'

# ID: (verdict, base kind, P100 reference, destino, a qué sirve / motivo)
D = {}
def put(ids, v, k, ref, dest, why):
    for i in ids:
        D[i] = (v, k, ref, dest, why)

# --- extinguished
for i in [1, 25, 26, 27, 70, 71, 72, 84, 90, 94, 102, 105, 119]:
    D[i] = ('Extinguida', None, None, None, None)

# --- state consultative bodies: Costes 2
put([8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 29, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 69],
    'Suprimir', EXP, 'Costes del Estado 2', 'Estructura ordinaria del ministerio, si alguna función es imprescindible',
    'Observatorio, consejo o comisión: el P100 los cierra salvo que su ministerio demuestre que su trabajo cambia decisiones o mejora un servicio; publicar informes no cuenta.')
# autonomic consultative bodies: same rule applied to CCAA
put([77, 85, 88, 123], 'Suprimir', INF, 'Costes del Estado 2 (aplicado a las CCAA)', 'Consejería',
    'Órgano consultivo sin medios propios: su producto son informes y reuniones, que el P100 no cuenta como resultado.')
put([115], 'Suprimir', INF, 'Costes del Estado 2 y 3 (aplicados a las CCAA)', None,
    'Órgano de representación juvenil: el P100 no financia entidades por existir.')

# --- state bodies with explicit P100 treatment
put([5], 'Mantener', EXP, 'Costes del Estado 1, 9 y 12; Organización del Estado 11', None,
    'Evalúa el gasto y los beneficios fiscales: el P100 le encarga revisar todo el gasto y conserva su informe obligatorio. Exigida por la UE.')
put([24], 'Mantener', EXP, 'Costes del Estado 9; Organización del Estado 11', None,
    'Regula mercados y sanciona conductas contra la competencia; el P100 conserva su informe obligatorio. Exigida por la UE.')
put([6], 'Reformar', EXP, 'Organización del Estado 11', None,
    'Resuelve las reclamaciones de acceso a la información; el P100 lo mantiene pero lo saca del alcance del Gobierno (terna por mérito, mandato único). Absorbería a los consejos autonómicos.')
put([31], 'Reformar', EXP, 'Costes del Estado 5', None,
    'Ejecuta la cooperación al desarrollo; el P100 deroga la senda del 0,7%, mantiene la ayuda humanitaria y concentra el resto en países que colaboren en el control migratorio.')
put([28], 'Mantener', EXP, 'Crecer y producir 16', None,
    'Inspecciona y sanciona los abusos en la cadena alimentaria: el P100 refuerza esa inspección («lo que se produce se cobra»). Exigida por la UE.')
put([30], 'Mantener', EXP, 'Inmigración 4 e Impuestos 3', None,
    'Inspecciona el trabajo y la Seguridad Social; el P100 le encarga perseguir la contratación irregular y los falsos autónomos.')
put([36], 'Reformar', EXP, 'Costes del Estado 10', None,
    'Gestiona viviendas e inmuebles de Defensa; el P100 obliga a inventariar sus suelos y a vender o ceder lo que no tenga uso.')
put([37, 38], 'Mantener', INF, 'Servicio directo; Menos normas 12 solo cambia el régimen de sus informes', None,
    'Confederación hidrográfica: organismo autónomo estatal que gestiona el agua de su cuenca; no duplica a ningún organismo autonómico. '
    'La medida 12 de «Menos normas» cambia el régimen de sus informes (silencio favorable y plazo único), pero es un cambio de procedimiento '
    'que afecta a todos los organismos que informan planes, igual que la medida 9 de Costes a la CNMC o la AIReF, que siguen en Mantener. '
    'Solo Miño-Sil y Cantábrico están en el inventario (creadas o transformadas desde 2004); el resto de cuencas no tiene ficha.')
put([66], 'Reformar', EXP, 'Crecer y producir 5', None,
    'Invierte los fondos del PERTE Chip y Next Tech; el P100 audita el PERTE Chip antes de comprometer un euro más y fija condiciones a quien recibe capital público.')
put([44], 'Integrar', EXP, 'Derogar el sanchismo; Organización del Estado 5', 'Defensor del Pueblo',
    'El P100 la suprime porque duplica funciones de otros organismos; sus garantías pasan al Defensor del Pueblo.')
put([22], 'Suprimir', EXP, 'Costes del Estado 2 y 3', None,
    'Fundación del sector público que reparte subvenciones a confesiones: el P100 cierra las fundaciones que no demuestren resultados y suprime las subvenciones por existir.')
put([107], 'Integrar', EXP, 'Organización del Estado 19', 'Instituciones Penitenciarias (Estado)',
    'Gestiona la reinserción de presos en el País Vasco; el P100 quiere que el Estado recupere la gestión de las prisiones.')
put([75, 80, 81, 86], 'Integrar', EXP, 'Impuestos y financiación territorial 11', 'Agencia Tributaria (AEAT)',
    'Gestiona tributos autonómicos y cedidos; el P100 quiere «una sola Agencia Tributaria» para todo el régimen común.')
put([97, 118, 120, 124], 'Integrar', EXP, 'Organización del Estado 17 y criterio Extramuros del 12/10/2026 («con una nacional basta»)', 'Agencia Estatal de Administración Digital y web única del Estado',
    'Agencia digital autonómica: el P100 hace una sola web y una sola aplicación para todo el Estado, a la que se suman las comunidades.')
put([73], 'Suprimir', EXP, 'Costes del Estado 5 y criterio Extramuros del 12/10/2026', None,
    'Cooperación autonómica al desarrollo: el P100 concentra la cooperación en el Estado y en países que colaboren en el control migratorio; una agencia autonómica no sirve a ese fin.')

# --- state bodies, P100 criterion (Costes 9: technical function, required impartiality or independent fact-finding that nobody else provides)
put([2], 'Mantener', INF, 'Costes del Estado 9 (función técnica; exigida por la UE)', None, 'Certifica e inspecciona la aviación civil; nadie más lo hace.')
put([7], 'Mantener', INF, 'Costes del Estado 9 (función técnica; exigida por la UE)', None, 'Certifica e inspecciona la seguridad de la red ferroviaria estatal.')
put([35], 'Mantener', INF, 'Costes del Estado 9 (función técnica; exigida por la UE)', None, 'Autoriza e inspecciona medicamentos y productos sanitarios.')
put([3], 'Mantener', INF, 'Costes del Estado 9 (independencia exigida por el Código Mundial Antidopaje)', None, 'Hace los controles antidopaje con la independencia que exige el código mundial.')
put([4], 'Mantener', INF, 'Costes del Estado 9 (función técnica)', None, 'Evalúa por pares y concede las ayudas estatales de investigación.')
put([33], 'Mantener', INF, 'Servicio directo', None, 'Investiga: unas 7.500 personas de su plantilla son científicos y otras 7.750 técnicos.')
put([34], 'Mantener', INF, 'Servicio directo', None, 'Predicción meteorológica y avisos; nadie más los presta.')
put([32], 'Mantener', INF, 'Servicio directo', None, 'Publica el BOE; se financia en buena parte con sus propios ingresos.')
put([39], 'Mantener', INF, 'Servicio directo (exigida por la UE)', None, 'Agencia nacional de Erasmus+, exigida por el reglamento europeo.')
put([41], 'Mantener', INF, 'Costes del Estado 9 (función técnica; exigida por la UE)', None, 'Vigila el mercado de la inteligencia artificial, como exige el reglamento europeo.')
put([42], 'Mantener', INF, 'Organización del Estado 17', None, 'Presta los servicios digitales comunes del Estado: es la pieza natural para la web única del P100.')
put([43], 'Mantener', INF, 'Costes del Estado 9 (imparcialidad; exigida por la UE)', None, 'Canal externo de denuncias y protección del informante, exigido por la directiva europea.')
put([23], 'Mantener', INF, 'Costes del Estado 9 (establecer hechos con independencia)', None, 'Supervisa la contratación pública con independencia; encaja con las medidas de competencia en licitaciones del P100.')
put([40], 'Integrar', INF, 'Costes del Estado 9 (alguien más ya lo hacía)', 'CDTI',
    'Canaliza programas espaciales y la aportación a la Agencia Espacial Europea, que el CDTI gestionaba hasta 2023; creada después de 2004.')
put([45], 'Integrar', INF, 'Costes del Estado 1 y 12', 'AIReF',
    'Evalúa políticas públicas, la misma función que el P100 encarga a la AIReF.')

# --- P100 does not decide yet
put([46], 'Pendiente de decisión', None, 'El P100 aún no tiene apartado de Sanidad', 'Con el criterio de Costes 9, el Ministerio de Sanidad',
    'Agencia de salud pública creada en 2025, sin presupuesto ni actividad acreditada; el Ministerio ya tiene vigilancia y alertas sanitarias.')
put([14], 'Pendiente de decisión', None, 'El P100 no trata la violencia de género ni el futuro del Ministerio de Igualdad', None,
    'Dirección general del Ministerio de Igualdad (no es un organismo): coordina la política contra la violencia de género y gestiona 79,5 M.')
put([65], 'Pendiente de decisión', None, 'El P100 no trata cultura', None, 'Museo estatal sin presupuesto propio, creado en 2023.')
put([106], 'Pendiente de decisión', None, 'El P100 no trata las televisiones autonómicas', None,
    'Radiotelevisión pública valenciana (81 M); RTVE ya tiene centros territoriales.')

# --- autonomic bodies: one national body is enough (criterio Extramuros del 12/10/2026)
put([74, 93], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026 («con una nacional basta»)', 'CNMC',
    'Autoridad autonómica de competencia; la CNMC ya actúa en todo el territorio.')
put([76], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026 y Organización del Estado 11', 'Consejo de Transparencia estatal y AEPD',
    'Consejo autonómico de transparencia y datos; el CTBG ya resuelve por convenio las reclamaciones de cinco comunidades y la AEPD supervisa por defecto.')
put([113], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'Consejo de Transparencia estatal',
    'Consejo asturiano que no funciona: Asturias firmó en 2026 un nuevo convenio con el CTBG.')
put([78, 99], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'ANECA',
    'Agencia autonómica de calidad universitaria; ANECA ya evalúa en las siete comunidades sin agencia propia.')
put([108, 110], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'CCN-CERT e INCIBE',
    'Agencia autonómica de ciberseguridad; el CCN-CERT es por ley el centro de referencia de todas las administraciones.')
put([104], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026 (exige cambiar la ley ferroviaria)', 'AESF',
    'Supervisa la seguridad de la red de FGV, que hoy la AESF no cubre por ley.')
put([89, 112, 117], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'AEI y CDTI (y la consejería para fondos propios)',
    'Agencia autonómica que financia I+D+i; la AEI y el CDTI ya financian en todo el territorio.')
put([122, 125], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'IDAE (y la consejería)',
    'Agencia autonómica de energía; el IDAE ya actúa en todo el territorio.')
put([98], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026 y Crecer y producir 5', 'Consejería e instrumentos estatales (ICO, ENISA, CDTI)',
    'Agencia andaluza de apoyo empresarial e internacionalización; esas funciones ya las cubren instrumentos estatales.')
put([91], 'Integrar', INF, 'Costes del Estado 9 (aplicado a las CCAA)', 'Consejería de turismo',
    'Promoción turística: no exige una entidad propia; la puede hacer la consejería.')
put([83], 'Integrar', INF, 'Costes del Estado 9 (aplicado a las CCAA)', 'Consejería (con el INSST como referencia técnica)',
    'Prevención de riesgos laborales: asistencia técnica que puede prestar la consejería.')
put([116], 'Integrar', INF, 'Costes del Estado 9 (aplicado a las CCAA)', 'Consejería',
    'Formación de funcionarios autonómicos: servicio interno que no exige una entidad propia.')
put([87, 92, 95], 'Integrar', INF, 'Criterio Extramuros del 12/10/2026', 'Cámara o Sindicatura de Cuentas y, para el canal de denuncias, la AIPI por convenio',
    'Oficina antifraude autonómica: investiga irregularidades que también ven el órgano de control externo y la Fiscalía.')
put([111], 'Integrar', INF, 'Costes del Estado 9 (aplicado a las CCAA)', 'Consejería de salud',
    'Agencia balear de salud pública sin capítulo de personal propio y con funcionamiento no confirmado.')
put([100], 'Suprimir', INF, 'Costes del Estado 9 (aplicado a las CCAA)', 'Consejería de salud',
    'No ha arrancado: 0 € de gasto de personal en 2025 y a marzo de 2026. Suprimirla cuesta menos que ponerla en marcha.')

# --- autonomic services nobody else provides
put([79, 101, 114], 'Mantener', INF, 'Servicio directo que el Estado no presta', None,
    'Bomberos, emergencias y 112: un servicio que el Estado no presta en ese territorio. '
    'Un «mando único» o integración operativa dentro de la comunidad (p. ej. 112, GREA e IESPA en Andalucía) no es el veredicto «Integrar» del P100: no hay organismo estatal que absorba el 112; los 17 centros son autonómicos.')
put([82], 'Mantener', INF, 'Servicio directo', None, 'Presta servicios sociales; el P100 fija reglas comunes, pero no vacía la competencia.')
put([96], 'Mantener', INF, 'Servicio directo', None, 'Apoyo jurídico a adultos con discapacidad (148 personas): un servicio exigido por ley.')
put([103], 'Mantener', INF, 'Función técnica y sancionadora', None, 'Persigue las infracciones urbanísticas graves.')
put([109], 'Mantener', INF, 'Servicio directo', None, 'Gestiona los puertos deportivos vascos con ingresos propios.')
put([121], 'Mantener', INF, 'Función técnica', None, 'Controla la calidad alimentaria y las denominaciones de origen gallegas, en línea con la soberanía alimentaria del P100.')

# --- altas del 14/10/2026 (observatorios estatales que faltaban)
put([126], 'Mantener', INF, 'Costes del Estado 2 y 9 (función técnica que nadie más presta)', None,
    'No es un órgano consultivo, sino la unidad de la DGT que produce la estadística de siniestralidad, lleva el Registro Nacional de Víctimas '
    'y prepara los planes de seguridad vial. Lo que sobra es el nombre de observatorio, no la función. Se creó sin aumento de gasto (DA 3.ª RD 1599/2004).')
put([127, 130, 132], 'Suprimir', EXP, 'Costes del Estado 2', 'Estructura ordinaria del ministerio, si alguna función es imprescindible',
    'Observatorio o consejo asesor: el P100 los cierra salvo que su ministerio demuestre que su trabajo cambia decisiones o mejora un servicio; publicar informes no cuenta.')
put([129], 'Suprimir', INF, 'Costes del Estado 2 (aplicado a una sociedad mercantil estatal)', 'Dirección de RTVE, si alguna función es imprescindible',
    'Observatorio interno de RTVE: su producto son informes y propuestas, que el P100 no cuenta como resultado. Su acuerdo de creación no está publicado.')
put([128], 'Suprimir', EXP, 'Costes del Estado 2 (creado por ley: se suprime en la ley de la medida 4)', 'Puertos del Estado, que ya elabora el informe anual de competitividad',
    'Observatorio de 42 miembros que hace recomendaciones no vinculantes sobre precios y calidad de los servicios portuarios; '
    'el informe anual de competitividad lo elabora Puertos del Estado por ley y puede seguir haciéndolo sin el observatorio.')
put([131], 'Suprimir', EXP, 'Costes del Estado 2 (creado por ley: se suprime en la ley de la medida 4)', 'Secretaría para la Unidad de Mercado, que ya lo gestiona',
    'Creado por ley en 2022 para hacer un catálogo de buenas prácticas regulatorias; no funciona como órgano diferenciado: lo gestiona la Secretaría para la Unidad de Mercado.')
put([133, 134], 'Suprimir', EXP, 'Costes del Estado 2', None,
    'Observatorio anunciado y no constituido: con el criterio del P100, que cierra los observatorios que no demuestren resultados, lo coherente es no crearlo.')
put([135], 'Suprimir', EXP, 'Costes del Estado 2 (los creados por ley se suprimen en la ley de la medida 4)', None,
    'Observatorio que el proyecto de ley del tabaco vuelve a crear, tras su supresión en 2014: con el criterio del P100 lo coherente es retirarlo del proyecto.')

IDS = ids_inventario()
assert sorted(D) == IDS, sorted(set(IDS) ^ set(D))
BIN = {'Mantener': 'Útil', 'Reformar': 'Útil', 'Integrar': 'No útil', 'Suprimir': 'No útil',
       'Pendiente de decisión': 'Sin decisión en el P100', 'Extinguida': 'Extinguida'}
out = []
from collections import Counter
cnt = Counter()
for i in IDS:
    v, k, ref, dest, why = D[i]
    cnt[v] += 1
    u = dict(prev[i]['updates'])
    u['Clasificación: útil / no útil'] = BIN[v]
    u['Clasificación: veredicto'] = v
    u['Clasificación: base en el P100'] = (f'{k}: {ref}' if k else ref) if ref else None
    u['Clasificación: destino de sus funciones'] = destino_para_mostrar(dest) if dest else dest
    if v != 'Extinguida':
        u['Clasificación: motivo'] = why
    e = {'ID': i, 'updates': u}
    if prev[i].get('fuentes_nuevas'):
        e['fuentes_nuevas'] = prev[i]['fuentes_nuevas']
    out.append(e)
json.dump(out, open(RES / 'Z_clasificacion.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(cnt, Counter(BIN[D[i][0]] for i in D))
