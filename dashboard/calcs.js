  // Every figure that is not a raw cell is worked out here, from the datasets.
  dash.calc('totales', {
    inputs: ['entidades'], title: 'Total de fichas',
    description: 'Fichas en la hoja y cuántas tienen presupuesto propio 2026.',
    fn: (entidades) => [{ fichas: entidades.length,
      con_presupuesto: entidades.filter((e) => e.presupuesto_anio === 2026 && e.presupuesto_m > 0).length }],
  });
  dash.calc('por_veredicto', {
    inputs: ['entidades'], title: 'Fichas por veredicto (P100)',
    description: 'Fichas, fichas con presupuesto propio 2026, suma de ese presupuesto (bases distintas, orden de magnitud) y fichas con actividad acreditada, por veredicto alineado con el P100.',
    fn: (entidades) => ['Mantener', 'Reformar', 'Integrar', 'Suprimir', 'Pendiente de decisión', 'Extinguida'].map((veredicto) => {
      const rows = entidades.filter((e) => e.veredicto === veredicto);
      const conP = rows.filter((e) => e.presupuesto_anio === 2026 && e.presupuesto_m > 0);
      return { veredicto, fichas: rows.length, con_presupuesto: conP.length,
        presupuesto_m: Math.round(conP.reduce((s, e) => s + e.presupuesto_m, 0) * 10) / 10,
        con_actividad: rows.filter((e) => e.actividad === 'Acreditada').length };
    }),
  });
  dash.calc('por_clase', {
    inputs: ['entidades'], title: 'Útil o no útil (P100)',
    description: 'Útil = Mantener o Reformar; No útil = Integrar o Suprimir; Sin decisión = el P100 no trata la materia; Extinguida.',
    fn: (entidades) => ['Útil', 'No útil', 'Sin decisión en el P100', 'Extinguida'].map((clase) => {
      const rows = entidades.filter((e) => e.clase === clase);
      const conP = rows.filter((e) => e.presupuesto_anio === 2026 && e.presupuesto_m > 0);
      return { clase, fichas: rows.length, con_presupuesto: conP.length,
        presupuesto_m: Math.round(conP.reduce((s, e) => s + e.presupuesto_m, 0) * 10) / 10 };
    }),
  });
  dash.calc('por_base', {
    inputs: ['entidades'], title: 'Base del veredicto en el P100',
    description: 'Fichas vigentes según si el P100 lo dice expresamente, si es una deducción a partir de su criterio, o si el P100 no trata la materia.',
    fn: (entidades) => ['Explícito en el P100', 'Aplicando el criterio del P100', 'El P100 no trata la materia']
      .map((base) => ({ base, fichas: entidades.filter((e) => e.base_tipo === base).length })),
  });
  dash.calc('integrar_destino', {
    inputs: ['entidades'], title: 'Integrar: a dónde iría cada función',
    description: 'Fichas con veredicto Integrar, con su presupuesto propio 2026 y el organismo que asumiría la función.',
    fn: (entidades) => entidades.filter((e) => e.veredicto === 'Integrar')
      .map((e) => ({ id: e.id, nombre: e.nombre, ccaa: e.ccaa, presupuesto_m: e.presupuesto_anio === 2026 ? e.presupuesto_m : null, destino: e.destino_mostrar || e.destino }))
      .sort((a, b) => (a.destino || '').localeCompare(b.destino || '', 'es') || (b.presupuesto_m || 0) - (a.presupuesto_m || 0)),
  });
  dash.calc('por_funcion', {
    inputs: ['entidades'], title: 'Fichas por función',
    description: 'Fichas y presupuesto propio 2026 (orden de magnitud) por tipo de función.',
    fn: (entidades) => ['Servicio público directo', 'Regulación o inspección de terceros', 'Financiación y ayudas',
      'Control interno y cumplimiento', 'Consultivo o participación', 'Extinguida o no constituida'].map((funcion) => {
      const rows = entidades.filter((e) => e.funcion === funcion);
      const conP = rows.filter((e) => e.presupuesto_anio === 2026 && e.presupuesto_m > 0);
      return { funcion, fichas: rows.length, presupuesto_m: Math.round(conP.reduce((s, e) => s + e.presupuesto_m, 0) * 10) / 10 };
    }),
  });
  dash.calc('coste_consultivos', {
    inputs: ['entidades'], title: 'Coste de personal de los órganos consultivos (escenario)',
    description: 'Órganos consultivos × personas a tiempo completo supuestas (1, 2 o 3) × coste por persona, que es la mediana de gasto de personal 2025 / personas ocupadas en las fichas que tienen ambos datos.',
    fn: (entidades) => {
      const organos = entidades.filter((e) => e.funcion === 'Consultivo o participación').length;
      const v = entidades.filter((e) => e.gasto_personal_2025_m > 0 && e.personas > 0)
        .map((e) => e.gasto_personal_2025_m * 1e6 / e.personas).sort((a, b) => a - b);
      const m = v.length % 2 ? v[(v.length - 1) / 2] : (v[v.length / 2 - 1] + v[v.length / 2]) / 2;
      const coste_persona = Math.round(m);
      return [1, 2, 3].map((n) => ({ clave: 'p' + n, escenario: n === 1 ? '1 persona por órgano' : n + ' personas por órgano',
        organos, coste_persona, coste_m: Math.round(organos * coste_persona * n / 1e5) / 10 }));
    },
  });
  dash.calc('por_periodo', {
    inputs: ['entidades'], title: 'Por presidencia',
    description: 'Fichas por veredicto según el periodo presidencial de creación o transformación.',
    fn: (entidades) => ['Zapatero', 'Rajoy', 'Sánchez'].map((periodo) => {
      const rows = entidades.filter((e) => e.periodo === periodo);
      const n = (v) => rows.filter((e) => e.veredicto === v).length;
      return { periodo, mantener: n('Mantener'), reformar: n('Reformar'), integrar: n('Integrar'), suprimir: n('Suprimir'),
        pendiente: n('Pendiente de decisión'), extinguida: n('Extinguida'), total: rows.length };
    }),
  });
  dash.calc('top_presupuesto', {
    inputs: ['entidades'], title: 'Mayores presupuestos 2026',
    description: 'Las 12 entidades con mayor presupuesto propio 2026.',
    fn: (entidades) => entidades.filter((e) => e.presupuesto_anio === 2026 && e.presupuesto_m > 0)
      .sort((a, b) => b.presupuesto_m - a.presupuesto_m).slice(0, 12)
      .map((e) => ({ id: e.id, nombre: e.nombre, veredicto: e.veredicto, presupuesto_m: e.presupuesto_m, presupuesto_base: e.presupuesto_base })),
  });
  dash.calc('gasto_resumen', {
    inputs: ['gasto_capitulos'], title: 'Funcionamiento propio frente a dinero de paso',
    description: 'Suma por entidad de los capítulos marcados como funcionamiento propio, de paso a terceros o sin desglosar.',
    fn: (gasto_capitulos) => ['CNMC', 'CSIC'].map((entidad) => {
      const r = gasto_capitulos.filter((g) => g.entidad === entidad);
      const s = (t) => Math.round(r.filter((g) => g.tipo === t).reduce((a, g) => a + g.importe_m, 0) * 10) / 10;
      const total = Math.round(r.reduce((a, g) => a + g.importe_m, 0) * 10) / 10;
      const propio = s('Funcionamiento propio');
      return { entidad, propio_m: propio, de_paso_m: s('De paso a terceros'), sin_desglosar_m: s('Sin desglosar'), total_m: total,
        pct_propio: Math.round(propio / total * 1000) / 10 };
    }),
  });
  dash.calc('temas_conteo', {
    inputs: ['duplicidades', 'temas'], title: 'Organismos por tema',
    description: 'Por tema: organismos verificados (estatal más comunidades con organismo o órgano propio) y comunidades sin verificar.',
    fn: (duplicidades, temas) => temas.map((t) => {
      const r = duplicidades.filter((d) => d.tema === t.tema);
      const estatal = r.filter((d) => d.tipo === 'estatal').length;
      const propios = r.filter((d) => d.tipo === 'ente' || d.tipo === 'organo').length;
      return { tema: t.tema, organismo_estatal: t.organismo_estatal, estatal, propios, total: estatal + propios,
        sin_verificar: r.filter((d) => d.tipo === 'no_verificado').length, cobertura_estatal: t.cobertura_estatal, competencia: t.competencia };
    }).sort((a, b) => b.total - a.total || a.tema.localeCompare(b.tema)),
  });
  dash.calc('grupos_hoja', {
    inputs: ['entidades'], title: 'Temas con varias entidades en la hoja',
    description: 'Temas funcionales con dos o más fichas en la hoja, con sus nombres y veredictos.',
    fn: (entidades) => {
      const by = {};
      entidades.forEach((e) => { (by[e.tema] = by[e.tema] || []).push(e); });
      return Object.keys(by).filter((k) => by[k].length > 1)
        .map((tema) => ({ tema, fichas: by[tema].length, entidades: by[tema].map((e) => `${e.nombre} (${e.veredicto})`).join('; ') }))
        .sort((a, b) => b.fichas - a.fichas || a.tema.localeCompare(b.tema));
    },
  });
  dash.calc('indicadores', {
    inputs: ['entidades', 'personal_desglose'], title: 'Indicadores comparables',
    description: 'Coste de personal 2025 por persona ocupada; capítulo 1 sobre presupuesto propio 2026; personal de administración sobre el total del desglose.',
    fn: (entidades, personal_desglose) => entidades.filter((e) => !e.referencia_matriz).map((e) => {
      const d = personal_desglose.find((p) => p.id === e.id);
      return { id: e.id, nombre: e.nombre, veredicto: e.veredicto,
        coste_persona: e.gasto_personal_2025_m > 0 && e.personas > 0 ? Math.round(e.gasto_personal_2025_m * 1e6 / e.personas) : null,
        pct_personal: e.cap1_m > 0 && e.presupuesto_m > 0 && e.presupuesto_anio === 2026 ? Math.round(e.cap1_m / e.presupuesto_m * 1000) / 10 : null,
        pct_admin: d && d.total > 0 && d.administracion != null ? Math.round(d.administracion / d.total * 1000) / 10 : null };
    }).filter((r) => r.coste_persona != null || r.pct_personal != null || r.pct_admin != null),
  });
  dash.calc('csic_resumen', {
    inputs: ['csic_personal'], title: 'CSIC por grupos',
    description: 'Suma de categorías del CSIC por grupo y peso mínimo y máximo de la administración.',
    fn: (csic_personal) => {
      const s = (g) => csic_personal.filter((r) => r.grupo === g).reduce((t, r) => t + r.personas, 0);
      const total = csic_personal.reduce((t, r) => t + r.personas, 0);
      const adm = s('Administración'); const sin = s('Sin asignar');
      return [{ cientificos: s('Científicos'), tecnicos: s('Técnicos'), administracion: adm, sin_asignar: sin, total,
        admin_min_pct: Math.round(adm / total * 1000) / 10, admin_max_pct: Math.round((adm + sin) / total * 1000) / 10 }];
    },
  });
  dash.calc('por_verificacion', {
    inputs: ['entidades'], title: 'Fichas por nivel de verificación',
    description: 'Cuántas fichas tienen cifras contrastadas dos veces, cifras con fuente oficial o ninguna cifra.',
    fn: (entidades) => ['Contrastada por un segundo revisor (muestra)', 'Fuente oficial citada', 'Sin cifras']
      .map((verificacion) => ({ verificacion, fichas: entidades.filter((e) => e.verificacion === verificacion).length })),
  });
  dash.calc('muestra_resumen', {
    inputs: ['verificacion_muestra'], title: 'Resultado de la muestra',
    description: 'Cifras de la muestra que coinciden con la fuente oficial.',
    fn: (verificacion_muestra) => [{ total: verificacion_muestra.length,
      coinciden: verificacion_muestra.filter((r) => r.resultado === 'COINCIDE').length }],
  });
  dash.calc('pendientes_resumen', {
    inputs: ['entidades'], title: 'Pendientes en fichas que se mantienen o se reforman',
    description: 'Fichas con veredicto Mantener o Reformar a las que les falta cada dato.',
    fn: (entidades) => {
      const u = entidades.filter((e) => (e.veredicto === 'Mantener' || e.veredicto === 'Reformar') && e.pendiente);
      const has = (k) => u.filter((e) => e.pendiente.split(', ').includes(k)).length;
      return [{ fichas: u.length, presupuesto: has('presupuesto 2026'), personas: has('personas'), desglose: has('desglose de personal') }];
    },
  });
