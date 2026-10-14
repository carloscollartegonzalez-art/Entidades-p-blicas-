# 1. Método de datos

La hoja original (`datos/entrada/`) ya traía un método estricto. Todo lo que se ha añadido lo respeta al pie de la letra. Estas reglas son las que hay que seguir si se amplía o actualiza.

## Reglas

1. **Solo fuentes primarias u oficiales:**
   - BOE y boletines autonómicos.
   - Leyes de presupuestos y sus anexos.
   - IGAE: ejecución mensual de organismos y cuentas anuales publicadas en el BOE.
   - Intervenciones generales y portales de presupuestos de las comunidades.
   - Portales de transparencia.
   - Cuentas anuales auditadas, memorias oficiales y RPT publicadas.

   La prensa sirve como pista para encontrar el documento, nunca como fuente de la cifra.
2. **Cada número lleva documento, página o tabla, unidad original y conversión.** La conversión aparece en la hoja «Verificación y pendientes» del Excel.
3. **Todo en millones de euros**, con hasta 6 decimales y sin redondear más de lo que permite la fuente. Por ejemplo, 20.513.203 € se escriben 20,513203.
4. **Nunca estimar, nunca prorratear.** No se reparte el presupuesto de un ministerio o de una consejería entre sus órganos.
5. **Nunca un 0 por «no encontrado».** Si no hay cifra, la celda queda vacía y el texto explica qué se buscó. Una celda vacía significa «sin cifra verificada», no cero.
6. **Año, base y corte siempre explícitos.** Hay que distinguir:
   - crédito inicial, crédito actualizado, obligaciones reconocidas y pagos;
   - presupuesto aprobado, proyecto y prórroga;
   - año completo y ejecución parcial.
7. **No se suman cifras de bases o cortes distintos.** El resumen de la hoja «Entidades» separa cada base y solo suma la ejecución con corte a 31/08/2026.

## Vocabulario controlado

La hoja resumen hace sus cálculos (SUMIFS) sobre estos literales, así que deben escribirse exactamente así.

- **Base del presupuesto numérico:** `Crédito total actualizado` | `Crédito inicial aprobado` | `Presupuesto propio aprobado`.
- **Estado de cuantificación:**
  - `Cifra propia verificada`
  - `Sin presupuesto propio: órgano sin dotación diferenciada (verificado en norma)`
  - `Sin cifra propia actual verificada`
  - los literales de extinción ya existentes en la hoja.
- **Corte de ejecución de personal:** por ejemplo, `Hasta 31/08/2026:8 meses, NO año completo`.

## Presupuesto y personal: qué es cada cosa

- **Presupuesto propio.** Es el crédito de la entidad, no su coste de funcionamiento. En varias entidades casi todo son transferencias a terceros:
  - **CNMC:** 98,3% (costes del sistema eléctrico, subastas de CO2, territorios no peninsulares, servicio postal).
  - **AEI, Agencia Espacial y AECID:** ayudas y programas.

  Por eso los totales son un orden de magnitud. Los 10.829 M€ de «crédito total actualizado» son la suma de 24 entidades con esa base. No son deuda ni gasto propio.
- **Capítulo 1 (gastos de personal).** No equivale a salarios: incluye cotizaciones sociales y otros conceptos. Hay tres columnas:
  - el crédito;
  - las obligaciones reconocidas (gasto ejecutado);
  - los pagos.
- **Personas frente a puestos.** «Personal: personas (ocupadas)» son efectivos reales. «Puestos aprobados / presupuestados» son plazas de RPT o del anexo de personal. Los vocales de un órgano colegiado no son plantilla.
- **Órganos sin presupuesto propio.** Se verifica en su norma de creación si dice «no supondrá incremento del gasto» o «se atenderá con los medios del Ministerio». Si un importe concreto los financia (un convenio, un encargo), va en las columnas contextuales («Importe contextual… NO sumar»), nunca como presupuesto propio.
- **Coste por persona.** La columna «Coste de personal por persona 2025 (EUR, calculado)» es una fórmula: gasto de personal 2025 dividido entre personas ocupadas. Solo aparece donde están los dos datos.

## Desglose del personal por tipo de puesto

Para las entidades con presupuesto propio se separa:
- **el núcleo:** técnicos, científicos, inspectores;
- **la administración y el apoyo;**
- **lo no clasificable;**
- **los puestos de libre designación, los altos cargos y el personal eventual.**

Hay dos criterios, y cada fila dice cuál usa en «Desglose: criterio de clasificación»:
- **Por función**, cuando la entidad publica categorías propias. Por ejemplo, el CSIC distingue investigadores, técnicos de apoyo y gestión.
- **Por grupo profesional, como aproximación.** A1 y A2 cuentan como núcleo; C1, C2 y E, como administración. Es un proxy: parte de los A1 y A2 hacen gestión.

## Niveles de verificación

| Nivel | Fichas | Qué significa |
|---|---|---|
| Contrastada por un segundo revisor (muestra) | 20 | Un agente que no participó en la búsqueda volvió a la fuente y comparó la cifra literal. Coincidieron 20 de 20. |
| Fuente oficial citada | 50 | Cada cifra tiene documento, página y unidad, pero no se ha recontrastado. |
| Sin cifras | 65 | Sobre todo órganos consultivos y entidades extinguidas, sin presupuesto propio que verificar. Incluye las 10 altas del 14/10/2026, ninguna con presupuesto propio. |

La clasificación (veredicto, función y duplicidad) es un juicio con criterio explícito, no un dato.

## Cobertura conseguida

| Campo | Hoja original | v6 |
|---|---|---|
| Presupuesto propio | 38 | 61 |
| Crédito de personal | 29 | 44 |
| Gasto de personal ejecutado | 22 | 33 |
| Gasto de personal 2025, año completo | 19 | 27 |
| Personas ocupadas | 4 | 29 |
| Puestos aprobados | 6 | 22 |

Hay 2.712 celdas cambiadas en las fichas originales. Cada una figura con su valor anterior y el nuevo en la hoja «Cambios 12-10-2026», que también registra las 10 altas del 14/10/2026 (fichas nuevas, en verde en la Hoja 1).
