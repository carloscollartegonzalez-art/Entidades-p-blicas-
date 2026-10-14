  const es = d3.formatLocale({ decimal: ',', thousands: '.', grouping: [3], currency: ['', ' €'] });
  const fInt = es.format(',d');
  const fM = es.format(',.1f');
  const fPct = es.format('.0%');
  const fmtM = (v) => (v == null ? '' : fM(v));
  const fmtN = (v) => (v == null ? '' : fInt(v));
  const VC = { 'Mantener': dash.colors[0], 'Reformar': dash.colors[1], 'Integrar': dash.colors[2], 'Suprimir': 'var(--cds-chart-status-critical)', 'Pendiente de decisión': dash.colors[3], 'Extinguida': 'var(--cds-chart-muted)' };
  const VCHIP = { 'Mantener': 'ep-chip--util', 'Reformar': 'ep-chip--ref', 'Integrar': 'ep-chip--rev', 'Suprimir': 'ep-chip--presc', 'Pendiente de decisión': 'ep-chip--pend', 'Extinguida': 'ep-chip--ext',
    'Referencia': 'ep-chip--pend', 'Útil': 'ep-chip--util', 'No útil': 'ep-chip--presc', 'Sin decisión en el P100': 'ep-chip--pend' };
  const VERS = ['Mantener', 'Reformar', 'Integrar', 'Suprimir', 'Pendiente de decisión', 'Extinguida'];
  const CLASES = ['Útil', 'No útil', 'Sin decisión en el P100', 'Extinguida'];
  const state = { page: 'resumen', q: '', clase: '', ver: '', fun: '', ambito: '', ccaa: '', sort: 'presupuesto_m', dir: -1, sel: null };
  const $ = (s) => document.querySelector(s);
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  const ok = (id) => dash.data(id).status === 'ok';
  const rows = (id) => (ok(id) ? dash.data(id).data : []);
  const safeUrl = (u) => (typeof u === 'string' && /^https:\/\//.test(u) ? u : null);
  const chip = (v) => el('span', 'ep-chip ' + (VCHIP[v] || ''), v);
  const short = (s, n) => { const m = s.match(/\(([^)]+)\)\s*$/); const b = s.replace(/^Agencia [Ee]statal /, ''); return m && m[1].length < 16 ? m[1] : (b.length > n ? b.slice(0, n - 1) + '…' : b); };
  let temaByName;
  const temaInfo = (nombre) => {
    if (!temaByName) temaByName = Object.fromEntries(rows('temas').map((t) => [t.tema, t]));
    return temaByName[nombre];
  };
  const TEMA_112 = 'Entes de emergencias 112';
  const NOTA_MATRIZ_112 = 'Sin organismo estatal (112 en las 17 CCAA)';
  const entidadesTabla = () => [...rows('entidades'), ...rows('referencias_matriz')];
  function textoMatrizIntegracion(e) {
    const dest = e.destino_mostrar || e.destino;
    if (e.veredicto === 'Integrar' && dest) return { text: dest, cls: 'ep-wrap', title: '' };
    if (e.tema === TEMA_112) {
      const ti = temaInfo(TEMA_112);
      const ref = ti && ti.organismo_estatal ? `Referencia estatal: ${ti.organismo_estatal} (no presta el 112).` : '';
      return { text: NOTA_MATRIZ_112, cls: 'ep-wrap ep-matriz--sin-estatal', title: ref };
    }
    return { text: '', cls: '', title: '' };
  }

  function failLine(node, id) {
    const st = dash.data(id).status;
    if (st === 'error' || st === 'connect' || st === 'declined') { node.replaceChildren(el('div', 'ep-fail', 'No se pudo cargar')); return true; }
    return false;
  }
  function fillMarks(root) {
    root.querySelectorAll('[data-source][data-field]').forEach((n) => {
      if (n.closest('table') || n.tagName === 'TH' || n.closest('#det-dl')) return;
      const id = n.getAttribute('data-source'); const f = n.getAttribute('data-field');
      const d = dash.data(id); if (d.status !== 'ok') { n.textContent = '—'; return; }
      let row = null;
      if (n.hasAttribute('data-row')) row = d.data[+n.getAttribute('data-row')];
      else if (n.hasAttribute('data-where')) {
        const [k, v] = n.getAttribute('data-where').split('=');
        row = d.data.find((r) => String(r[k]) === decodeURIComponent(v));
      }
      const v = row ? row[f] : null;
      if (v == null) { n.textContent = '—'; return; }
      n.textContent = typeof v === 'number' ? (Number.isInteger(v) ? fInt(v) : fM(v)) : v;
      n.classList.remove('dash-skeleton');
    });
  }
  function tipFor(box) { let t = box.querySelector('.ep-tip'); if (!t) { t = el('div', 'ep-tip'); t.hidden = true; box.appendChild(t); } return t; }
  function showTip(box, ev, head, lines) {
    const t = tipFor(box);
    t.replaceChildren(el('div', 'ep-tip-h', head), ...lines.map(([c, txt]) => {
      const d = el('div'); if (c) { const s = el('span', 'ep-sw'); s.style.background = c; d.appendChild(s); } d.appendChild(document.createTextNode(txt)); return d;
    }));
    t.hidden = false;
    const r = box.getBoundingClientRect();
    let x = ev.clientX - r.left + 12, y = ev.clientY - r.top + 12;
    if (x + t.offsetWidth > box.clientWidth) x = Math.max(0, ev.clientX - r.left - t.offsetWidth - 12);
    if (y + t.offsetHeight > box.clientHeight + 40) y = Math.max(0, ev.clientY - r.top - t.offsetHeight - 12);
    t.style.left = x + 'px'; t.style.top = y + 'px';
  }
  function hideTip(box) { const t = box.querySelector('.ep-tip'); if (t) t.hidden = true; }
  function legend(node, items, opac) {
    node.replaceChildren(...items.map(([c, txt, o, dashed]) => { const d = el('span'); const s = el('span', 'ep-sw'); s.style.background = dashed ? 'transparent' : c; if (dashed) s.style.border = '1px dashed var(--color-fg-muted)'; if (o != null) s.style.opacity = o; d.append(s, document.createTextNode(txt)); return d; }));
  }
  function inBar(v, max, color, txt) {
    const td = el('td', 'ep-num'); const w = el('div', 'ep-bar-cell'); const b = el('span', 'ep-inbar');
    b.style.width = Math.max(1, (max ? v / max : 0) * 90) + 'px'; b.style.background = color; w.append(b, el('span', null, txt)); td.appendChild(w); return td;
  }

  // ---------- RESUMEN ----------
  function drawResumen() {
    const pv = rows('por_veredicto'); const maxF = d3.max(pv, (d) => d.fichas) || 1; const maxP = d3.max(pv, (d) => d.presupuesto_m) || 1;
    $('#tabla-veredicto tbody').replaceChildren(...pv.map((d) => {
      const tr = el('tr'); tr.dataset.key = d.veredicto; const c = el('td'); c.appendChild(chip(d.veredicto));
      tr.append(c, inBar(d.fichas, maxF, VC[d.veredicto], fInt(d.fichas)), el('td', 'ep-num', fInt(d.con_presupuesto)), inBar(d.presupuesto_m, maxP, VC[d.veredicto], fM(d.presupuesto_m)));
      return tr;
    }));
    const pc = rows('por_clase'); const mcF = d3.max(pc, (d) => d.fichas) || 1; const mcP = d3.max(pc, (d) => d.presupuesto_m) || 1;
    const CC = { 'Útil': dash.colors[0], 'No útil': 'var(--cds-chart-status-critical)', 'Sin decisión en el P100': dash.colors[3], 'Extinguida': 'var(--cds-chart-muted)' };
    $('#tabla-clase tbody').replaceChildren(...pc.map((d) => {
      const tr = el('tr'); tr.dataset.key = d.clase; const c = el('td'); c.appendChild(chip(d.clase));
      tr.append(c, inBar(d.fichas, mcF, CC[d.clase], fInt(d.fichas)), el('td', 'ep-num', fInt(d.con_presupuesto)), inBar(d.presupuesto_m, mcP, CC[d.clase], fM(d.presupuesto_m)));
      return tr;
    }));
    $('#tabla-base tbody').replaceChildren(...rows('por_base').map((d) => { const tr = el('tr'); tr.dataset.key = d.base; tr.append(el('td', null, d.base), el('td', 'ep-num', fInt(d.fichas))); return tr; }));
    $('#tabla-integrar tbody').replaceChildren(...rows('integrar_destino').map((d) => {
      const tr = el('tr'); tr.dataset.key = String(d.id); const de = el('td'); de.appendChild(el('span', 'ep-wrap', d.destino || ''));
      tr.append(el('td', 'ep-name', d.nombre), el('td', null, d.ccaa), el('td', 'ep-num', fmtM(d.presupuesto_m)), de); return tr;
    }));
    const pf = rows('por_funcion'); const mf = d3.max(pf, (d) => d.fichas) || 1; const mp = d3.max(pf, (d) => d.presupuesto_m) || 1;
    $('#tabla-funcion tbody').replaceChildren(...pf.map((d) => {
      const tr = el('tr'); tr.dataset.key = d.funcion;
      tr.append(el('td', null, d.funcion), inBar(d.fichas, mf, 'var(--cds-chart-muted)', fInt(d.fichas)), inBar(d.presupuesto_m, mp, 'var(--cds-chart-muted)', fM(d.presupuesto_m)));
      return tr;
    }));
    $('#tabla-coste tbody').replaceChildren(...rows('coste_consultivos').map((d) => {
      const tr = el('tr'); tr.dataset.key = d.clave;
      tr.append(el('td', null, d.escenario), el('td', 'ep-num', fInt(d.organos)), el('td', 'ep-num', fInt(d.coste_persona)), el('td', 'ep-num', fM(d.coste_m)));
      return tr;
    }));
    drawPeriodo(); drawGasto(); drawTop();
  }
  function drawPeriodo() {
    const box = $('#chart-periodo'); if (failLine(box, 'entidades')) return;
    const data = rows('por_periodo'); if (!data.length) return;
    const W = box.clientWidth || 400; const rowH = 34, left = 70, right = 36; const H = data.length * rowH;
    const keys = [['mantener', 'Mantener'], ['reformar', 'Reformar'], ['integrar', 'Integrar'], ['suprimir', 'Suprimir'], ['pendiente', 'Pendiente de decisión'], ['extinguida', 'Extinguida']];
    const x = d3.scaleLinear([0, d3.max(data, (d) => d.total)], [0, Math.max(40, W - left - right)]);
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const g = svg.selectAll('g').data(data).join('g').attr('transform', (d, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', 0).attr('y', 16).attr('dy', '.35em').attr('class', 'ep-lbl-strong').text((d) => d.periodo);
    keys.forEach(([k, v], idx) => {
      g.append('rect').attr('y', 6).attr('height', 20)
        .attr('x', (d) => left + x(keys.slice(0, idx).reduce((s, [kk]) => s + d[kk], 0)))
        .attr('width', (d) => Math.max(0, x(d[k]) - (d[k] ? 1 : 0))).style('fill', VC[v]);
    });
    g.append('text').attr('x', (d) => left + x(d.total) + 6).attr('y', 16).attr('dy', '.35em').text((d) => fInt(d.total));
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).style('fill', 'transparent')
      .on('mousemove', (ev, d) => showTip(box, ev, d.periodo, keys.map(([k, v]) => [VC[v], `${v}: ${fInt(d[k])}`])))
      .on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
    legend($('#legend-periodo'), VERS.map((v) => [VC[v], v]));
  }
  function drawGasto() {
    const box = $('#chart-gasto'); if (failLine(box, 'gasto_capitulos')) return;
    const data = rows('gasto_resumen'); if (!data.length) return;
    const W = box.clientWidth || 600; const rowH = 44, left = 56, right = 8; const H = data.length * rowH;
    const parts = [['propio_m', 'Funcionamiento propio', dash.colors[0]], ['de_paso_m', 'De paso a terceros', 'var(--cds-chart-muted)'], ['sin_desglosar_m', 'Sin desglosar', dash.colors[2]]];
    const bw = Math.max(80, W - left - right);
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const g = svg.selectAll('g').data(data).join('g').attr('transform', (d, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', 0).attr('y', 14).attr('dy', '.35em').attr('class', 'ep-lbl-strong').text((d) => d.entidad);
    parts.forEach(([k, , c], idx) => {
      g.append('rect').attr('y', 4).attr('height', 20).attr('x', (d) => left + bw * parts.slice(0, idx).reduce((s, [kk]) => s + d[kk], 0) / d.total_m)
        .attr('width', (d) => Math.max(0, bw * d[k] / d.total_m - (d[k] ? 1 : 0))).style('fill', c);
    });
    g.append('text').attr('x', left).attr('y', 36).text((d) => `Funcionamiento propio ${fM(d.propio_m)} M€ (${String(d.pct_propio).replace('.', ',')} %) de ${fM(d.total_m)} M€`);
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).style('fill', 'transparent')
      .on('mousemove', (ev, d) => showTip(box, ev, d.entidad, parts.filter(([k]) => d[k]).map(([k, lab, c]) => [c, `${lab}: ${fM(d[k])} M€`])))
      .on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
    legend($('#legend-gasto'), parts.map(([, lab, c]) => [c, lab]));
    $('#tabla-gasto tbody').replaceChildren(...rows('gasto_capitulos').map((d) => {
      const tr = el('tr'); tr.dataset.key = d.clave; const de = el('td'); de.appendChild(el('span', 'ep-wrap', d.destino || ''));
      tr.append(el('td', null, d.entidad), el('td', null, d.concepto), el('td', 'ep-num', fM(d.importe_m)), el('td', null, d.tipo), de); return tr;
    }));
  }
  function drawTop() {
    const box = $('#chart-top'); if (failLine(box, 'entidades')) return;
    const data = rows('top_presupuesto'); if (!data.length) return;
    const W = box.clientWidth || 600; const rowH = 28; const H = data.length * rowH + 4;
    const left = Math.min(Math.max(90, W * 0.32), 230);
    const x = d3.scaleLinear([0, d3.max(data, (d) => d.presupuesto_m)], [0, Math.max(40, W - left - 64)]);
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const g = svg.selectAll('g').data(data).join('g').attr('transform', (d, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', left - 8).attr('y', 13).attr('dy', '.35em').attr('text-anchor', 'end').attr('class', 'ep-lbl-strong').text((d) => short(d.nombre, 34));
    g.append('rect').attr('x', left).attr('y', 4).attr('height', 18).attr('rx', 4).attr('width', (d) => Math.max(1, x(d.presupuesto_m))).style('fill', (d) => VC[d.veredicto]);
    g.append('text').attr('x', (d) => left + x(d.presupuesto_m) + 6).attr('y', 13).attr('dy', '.35em').text((d) => fM(d.presupuesto_m));
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).style('fill', 'transparent')
      .on('mousemove', (ev, d) => showTip(box, ev, d.nombre, [[VC[d.veredicto], `${fM(d.presupuesto_m)} M€ · ${d.presupuesto_base || ''}`], [null, d.veredicto]]))
      .on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
    legend($('#legend-veredicto'), VERS.map((v) => [VC[v], v]));
  }

  // ---------- DUPLICIDADES ----------
  const TIPO_STYLE = {
    estatal: [dash.colors[0], 1, 'Organismo estatal'], ente: ['var(--cds-chart-status-critical)', 1, 'Organismo autonómico propio (con personalidad)'],
    organo: ['var(--cds-chart-status-critical)', 0.5, 'Órgano autonómico propio (sin personalidad)'], estado: [dash.colors[0], 0.22, 'Lo cubre el organismo estatal'],
    consejeria: ['var(--cds-chart-muted)', 0.45, 'Lo hace la consejería'], no: ['var(--cds-chart-muted)', 0.2, 'No existe'],
    no_verificado: ['var(--cds-chart-muted)', 0, 'Sin verificar'],
  };
  function drawMatriz() {
    const box = $('#chart-matriz'); if (failLine(box, 'duplicidades')) return;
    const temas = rows('temas_conteo'); const dup = rows('duplicidades'); if (!temas.length || !dup.length) return;
    const cols = ['Estado', 'Andalucía', 'Aragón', 'Asturias', 'Illes Balears', 'Canarias', 'Cantabria', 'Castilla-La Mancha', 'Castilla y León', 'Cataluña', 'Comunitat Valenciana', 'Extremadura', 'Galicia', 'Madrid', 'Murcia', 'Navarra', 'País Vasco', 'La Rioja'];
    const abbr = {}; dup.forEach((d) => { abbr[d.territorio] = d.abrev; });
    const avail = Math.max(box.parentElement.clientWidth || 700, 640);
    const left = Math.min(260, Math.max(170, avail * 0.28)); const cw = Math.max(22, Math.min(36, (avail - left - 40) / cols.length));
    const ch = 24; const top = 28; const W = left + cols.length * cw + 40; const H = top + temas.length * ch + 4;
    const idx = {}; dup.forEach((d) => { idx[d.tema + '|' + d.territorio] = d; });
    const svg = d3.create('svg').attr('width', W).attr('height', H).attr('viewBox', `0 0 ${W} ${H}`);
    svg.selectAll('text.ep-col').data(cols).join('text').attr('class', 'ep-col').attr('x', (c, i) => left + i * cw + cw / 2).attr('y', top - 10).attr('text-anchor', 'middle').text((c) => abbr[c] || c);
    const g = svg.selectAll('g.r').data(temas).join('g').attr('class', 'r').attr('transform', (d, i) => `translate(0,${top + i * ch})`);
    g.append('text').attr('x', left - 8).attr('y', ch / 2).attr('dy', '.35em').attr('text-anchor', 'end').attr('class', 'ep-lbl-strong').text((d) => (d.tema.length > 40 ? d.tema.slice(0, 39) + '…' : d.tema));
    g.each(function (t) {
      const gg = d3.select(this);
      cols.forEach((c, i) => {
        const d = idx[t.tema + '|' + c]; const st = TIPO_STYLE[d ? d.tipo : 'no_verificado'] || TIPO_STYLE.no_verificado;
        const r = gg.append('rect').attr('x', left + i * cw + 1).attr('y', 2).attr('width', cw - 2).attr('height', ch - 4).attr('rx', 3)
          .style('fill', st[1] ? st[0] : 'transparent').style('fill-opacity', st[1] || 0);
        if (!st[1]) r.style('stroke', 'var(--cds-chart-muted)').style('stroke-dasharray', '2 2');
        r.on('mousemove', (ev) => showTip(box, ev, `${t.tema} · ${c}`, [[st[1] ? st[0] : null, st[2]], [null, (d && d.nombre) || '—']]))
          .on('mouseleave', () => hideTip(box));
      });
      gg.append('text').attr('x', left + cols.length * cw + 8).attr('y', ch / 2).attr('dy', '.35em').attr('class', 'ep-lbl-strong').text(fInt(t.total));
    });
    box.style.width = W + 'px';
    box.replaceChildren(svg.node());
    legend($('#legend-matriz'), ['estatal', 'ente', 'organo', 'estado', 'consejeria', 'no', 'no_verificado'].map((k) => [TIPO_STYLE[k][0], TIPO_STYLE[k][2], TIPO_STYLE[k][1] || null, !TIPO_STYLE[k][1]]));
  }
  function drawTemas() {
    const box = $('#chart-temas'); if (failLine(box, 'duplicidades')) return;
    const data = rows('temas_conteo'); if (!data.length) return;
    const W = box.clientWidth || 420; const rowH = 24; const H = data.length * rowH + 4;
    const left = Math.min(Math.max(120, W * 0.45), 250);
    const x = d3.scaleLinear([0, 18], [0, Math.max(40, W - left - 34)]);
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    svg.append('line').attr('x1', left + x(18)).attr('x2', left + x(18)).attr('y1', 0).attr('y2', H).style('stroke', 'var(--cds-chart-reference)').style('stroke-dasharray', '3 3');
    const g = svg.selectAll('g').data(data).join('g').attr('transform', (d, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', left - 8).attr('y', 11).attr('dy', '.35em').attr('text-anchor', 'end').attr('class', 'ep-lbl-strong').text((d) => (d.tema.length > 34 ? d.tema.slice(0, 33) + '…' : d.tema));
    g.append('rect').attr('x', left).attr('y', 3).attr('height', 16).attr('rx', 3).attr('width', (d) => Math.max(1, x(d.total))).style('fill', 'var(--cds-chart-status-critical)');
    g.append('rect').attr('x', (d) => left + x(d.total)).attr('y', 3).attr('height', 16).attr('width', (d) => Math.max(0, x(d.sin_verificar))).style('fill', 'var(--cds-chart-muted)').style('opacity', .35);
    g.append('text').attr('x', (d) => left + x(d.total + d.sin_verificar) + 5).attr('y', 11).attr('dy', '.35em').text((d) => fInt(d.total));
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).style('fill', 'transparent')
      .on('mousemove', (ev, d) => showTip(box, ev, d.tema, [['var(--cds-chart-status-critical)', `Organismos verificados: ${fInt(d.total)} (estatal: ${fInt(d.estatal)})`], ['var(--cds-chart-muted)', `Comunidades sin verificar: ${fInt(d.sin_verificar)}`]]))
      .on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
    $('#tabla-temas tbody').replaceChildren(...data.map((d) => {
      const tr = el('tr'); tr.dataset.key = d.tema; const cob = el('td'); cob.appendChild(el('span', 'ep-wrap', d.cobertura_estatal || ''));
      tr.append(el('td', 'ep-name', d.tema), el('td', 'ep-num', fInt(d.total)), el('td', null, d.organismo_estatal), cob); return tr;
    }));
    $('#tabla-grupos tbody').replaceChildren(...rows('grupos_hoja').map((d) => {
      const tr = el('tr'); tr.dataset.key = d.tema; const en = el('td'); en.appendChild(el('span', 'ep-wrap', d.entidades));
      tr.append(el('td', 'ep-name', d.tema), el('td', 'ep-num', fInt(d.fichas)), en); return tr;
    }));
  }

  // ---------- ENTIDADES ----------
  let filtersBuilt = false;
  function buildFilters() {
    if (filtersBuilt || !ok('entidades')) return;
    const data = rows('entidades');
    $('#f-clase').append(...CLASES.map((n) => new Option(n, n)));
    $('#f-ver').append(...VERS.map((n) => new Option(n, n)));
    $('#f-fun').append(...[...new Set(data.map((e) => e.funcion))].sort().map((n) => new Option(n, n)));
    $('#f-ccaa').append(...[...new Set(data.filter((e) => e.ambito === 'Autonómico').map((e) => e.ccaa))].sort((a, b) => a.localeCompare(b, 'es')).map((n) => new Option(n, n)));
    filtersBuilt = true;
  }
  function filtered() {
    const q = state.q.trim().toLowerCase();
    let d = entidadesTabla().filter((e) => (!state.clase || e.clase === state.clase) && (!state.ver || e.veredicto === state.ver) && (!state.fun || e.funcion === state.fun) &&
      (!state.ambito || e.ambito === state.ambito) && (!state.ccaa || e.ccaa === state.ccaa) &&
      (!q || [e.nombre, e.ccaa, e.motivo, e.tema, e.funcion, e.base_p100, e.destino, textoMatrizIntegracion(e).text].join(' ').toLowerCase().includes(q)));
    const k = state.sort, dir = state.dir;
    return d.slice().sort((a, b) => { const va = a[k], vb = b[k]; if (va == null && vb == null) return 0; if (va == null) return 1; if (vb == null) return -1;
      return (typeof va === 'number' ? va - vb : String(va).localeCompare(String(vb), 'es')) * dir; });
  }
  function drawTabla() {
    buildFilters();
    const data = filtered();
    const nRef = data.filter((e) => e.referencia_matriz).length;
    const nEnt = data.length - nRef;
    $('#f-count').textContent = ok('entidades') ? `Mostrando ${fInt(nEnt)} de ${fInt(rows('entidades').length)} entidades${nRef ? ` y ${fInt(nRef)} ${nRef === 1 ? 'fila' : 'filas'} de referencia` : ''}` : '';
    document.querySelectorAll('#tabla-entidades th').forEach((th) => { const f = th.getAttribute('data-field'); th.setAttribute('aria-sort', f === state.sort ? (state.dir > 0 ? 'ascending' : 'descending') : 'none'); });
    $('#tabla-entidades tbody').replaceChildren(...data.map((e) => {
      const tr = el('tr', 'ep-click' + (state.sel === e.id ? ' ep-sel' : '')); tr.dataset.key = String(e.id);
      const cv = el('td'); cv.appendChild(chip(e.veredicto));
      const mi = textoMatrizIntegracion(e);
      const md = el('td');
      if (mi.text) { const sp = el('span', mi.cls, mi.text); if (mi.title) sp.title = mi.title; md.appendChild(sp); }
      const ct = el('td'); ct.appendChild(el('span', 'ep-clip', e.tema || ''));
      tr.append(el('td', 'ep-name', e.nombre), el('td', null, e.ccaa), cv, md, el('td', null, e.funcion), ct,
        el('td', 'ep-num', e.referencia_matriz && e.presupuesto_m != null ? `${fmtM(e.presupuesto_m)} (${e.presupuesto_anio})` : fmtM(e.presupuesto_m)), el('td', 'ep-num', fmtM(e.cap1_m)), el('td', 'ep-num', fmtN(e.personas)), el('td', null, e.verificacion));
      return tr;
    }));
    drawDetalle();
  }
  function drawDetalle() {
    const box = $('#detalle'); const e = entidadesTabla().find((r) => r.id === state.sel);
    if (!e) { box.hidden = true; return; }
    box.hidden = false;
    $('#det-nombre').textContent = e.nombre;
    $('#det-motivo').textContent = `${e.veredicto} (${e.clase}) · ${e.funcion}. ${e.motivo || ''}`;
    const items = [
      ['Base en el P100', 'base_p100', e.base_p100, null], ['Destino de sus funciones', 'destino', e.destino_mostrar || e.destino, null],
      ['Duplicidad', 'duplicidad', e.duplicidad, null], ['Exigida por la UE', 'ue', e.ue, null], ['Tema', 'tema', e.tema, null],
      ['Presupuesto propio (M€)', 'presupuesto_m', fmtM(e.presupuesto_m), [e.presupuesto_base, e.presupuesto_corte].filter(Boolean).join(' · ')],
      ['Personal, cap. 1 (M€)', 'cap1_m', fmtM(e.cap1_m), null],
      ['Gasto de personal ejecutado (M€)', 'gasto_personal_m', fmtM(e.gasto_personal_m), e.gasto_personal_corte],
      ['Gasto de personal 2025, año completo (M€)', 'gasto_personal_2025_m', fmtM(e.gasto_personal_2025_m), null],
      ['Personas ocupadas', 'personas', fmtN(e.personas), e.personas_fecha], ['Plazas o puestos', 'plazas', fmtN(e.plazas), null],
      ['Coste de apoyo (sin presupuesto propio)', 'apoyo', e.apoyo, null],
      ['Importe de contexto, no sumar (M€)', 'contextual_m', fmtM(e.contextual_m), e.contextual_base],
      ['Actividad reciente', 'actividad', e.actividad, null], ['Verificación', 'verificacion', e.verificacion, null], ['Falta', 'pendiente', e.pendiente, null],
    ].filter((it) => it[2]);
    const dl = $('#det-dl');
    dl.replaceChildren(...items.map(([lab, field, val, note]) => {
      const d = el('div'); const dd = el('dd'); const v = el('span', null, val);
      v.setAttribute('data-source', 'entidades'); v.setAttribute('data-field', field); v.setAttribute('data-where', 'id=' + e.id);
      dd.appendChild(v); if (note) dd.appendChild(el('div', 'ep-note', note)); d.append(el('dt', null, lab), dd); return d;
    }));
    const u = safeUrl(e.fuente);
    if (u) { const d = el('div'); const dd = el('dd'); const a = el('a', null, 'Abrir la fuente principal'); a.href = u; a.target = '_blank'; a.rel = 'noopener'; dd.appendChild(a); d.append(el('dt', null, 'Fuente'), dd); dl.appendChild(d); }
  }

  // ---------- PERSONAL ----------
  function drawCsic() {
    const box = $('#chart-csic'); if (failLine(box, 'csic_personal')) return;
    const data = rows('csic_personal'); if (!data.length) return;
    const total = d3.sum(data, (d) => d.personas); const W = box.clientWidth || 600; const H = 28;
    const col = { 'Científicos': dash.colors[0], 'Técnicos': dash.colors[2], 'Administración': 'var(--color-warn)', 'Sin asignar': 'var(--cds-chart-muted)' };
    const x = d3.scaleLinear([0, total], [0, W]); let acc = 0; const segs = data.map((d) => { const s = { ...d, x0: acc }; acc += d.personas; return s; });
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    svg.selectAll('rect').data(segs).join('rect').attr('x', (d) => x(d.x0)).attr('y', 2).attr('height', 22).attr('width', (d) => Math.max(0, x(d.personas) - 1)).style('fill', (d) => col[d.grupo])
      .on('mousemove', (ev, d) => showTip(box, ev, d.categoria, [[col[d.grupo], `${fInt(d.personas)} personas · ${fPct(d.personas / total)}`]])).on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
  }
  function drawDesglose() {
    const box = $('#chart-desglose'); if (failLine(box, 'personal_desglose')) return;
    const data = rows('personal_desglose').filter((d) => d.total > 0).sort((a, b) => b.total - a.total); if (!data.length) return;
    const W = box.clientWidth || 700; const rowH = 24; const H = data.length * rowH + 4;
    const left = Math.min(Math.max(110, W * 0.34), 260); const bw = Math.max(60, W - left - 64);
    const C = [['nucleo', dash.colors[0], 'Núcleo técnico, científico o inspector'], ['administracion', 'var(--color-warn)', 'Administración y apoyo'], ['otro', 'var(--cds-chart-muted)', 'Otro o no clasificable']];
    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('height', H);
    const g = svg.selectAll('g').data(data).join('g').attr('transform', (d, i) => `translate(0,${i * rowH})`);
    g.append('text').attr('x', left - 8).attr('y', 11).attr('dy', '.35em').attr('text-anchor', 'end').attr('class', 'ep-lbl-strong').text((d) => short(d.nombre, 38));
    C.forEach(([k, c], idx) => { g.append('rect').attr('y', 3).attr('height', 16).attr('x', (d) => left + bw * C.slice(0, idx).reduce((s, [kk]) => s + (d[kk] || 0), 0) / d.total)
      .attr('width', (d) => Math.max(0, bw * (d[k] || 0) / d.total - (d[k] ? 1 : 0))).style('fill', c); });
    g.append('text').attr('x', left + bw + 6).attr('y', 11).attr('dy', '.35em').text((d) => fInt(d.total));
    g.append('rect').attr('x', 0).attr('y', 0).attr('width', W).attr('height', rowH).style('fill', 'transparent')
      .on('mousemove', (ev, d) => showTip(box, ev, d.nombre, [...C.map(([k, c, lab]) => [c, `${lab}: ${fmtN(d[k]) || '—'} (${fPct((d[k] || 0) / d.total)})`]), [null, d.unidad_fecha || '']])).on('mouseleave', () => hideTip(box));
    box.replaceChildren(svg.node());
    legend($('#legend-desglose'), C.map(([, c, lab]) => [c, lab]));
    $('#tabla-ld tbody').replaceChildren(...rows('personal_desglose').slice().sort((a, b) => (b.total || 0) - (a.total || 0)).map((d) => {
      const tr = el('tr'); tr.dataset.key = String(d.id); const name = el('td', 'ep-name'); const u = safeUrl(d.fuente);
      if (u) { const a = el('a', null, d.nombre); a.href = u; a.target = '_blank'; a.rel = 'noopener'; name.appendChild(a); } else name.textContent = d.nombre;
      const uf = el('td'); uf.appendChild(el('span', 'ep-clip', d.unidad_fecha || '')); const cr = el('td'); cr.appendChild(el('span', 'ep-clip', d.criterio || ''));
      tr.append(name, ...['total', 'nucleo', 'administracion', 'libre_designacion', 'altos_cargos', 'eventuales'].map((k) => el('td', 'ep-num', fmtN(d[k]))), uf, cr); return tr;
    }));
  }

  // ---------- INDICADORES ----------
  function drawInd() {
    const data = rows('indicadores').slice().sort((a, b) => VERS.indexOf(a.veredicto) - VERS.indexOf(b.veredicto) || a.nombre.localeCompare(b.nombre, 'es'));
    const pc = (v) => (v == null ? '' : String(v).replace('.', ','));
    $('#tabla-ind tbody').replaceChildren(...data.map((d) => {
      const tr = el('tr'); tr.dataset.key = String(d.id); const cv = el('td'); cv.appendChild(chip(d.veredicto));
      tr.append(el('td', 'ep-name', d.nombre), cv, el('td', 'ep-num', fmtN(d.coste_persona)), el('td', 'ep-num', pc(d.pct_personal)), el('td', 'ep-num', pc(d.pct_admin))); return tr;
    }));
  }

  // ---------- VERIFICACIÓN ----------
  function drawVerif() {
    $('#tabla-verif tbody').replaceChildren(...rows('por_verificacion').map((d) => { const tr = el('tr'); tr.dataset.key = d.verificacion; tr.append(el('td', null, d.verificacion), el('td', 'ep-num', fInt(d.fichas))); return tr; }));
    $('#tabla-muestra tbody').replaceChildren(...rows('verificacion_muestra').map((d) => {
      const tr = el('tr'); tr.dataset.key = String(d.id); const name = el('td', 'ep-name'); const u = safeUrl(d.url);
      if (u) { const a = el('a', null, d.nombre); a.href = u; a.target = '_blank'; a.rel = 'noopener'; name.appendChild(a); } else name.textContent = d.nombre;
      const res = el('td'); res.appendChild(el('span', d.resultado === 'COINCIDE' ? 'ep-chip ep-chip--util' : 'ep-chip ep-chip--presc', d.resultado));
      const vh = typeof d.valor_hoja === 'number' ? (Number.isInteger(d.valor_hoja) ? fInt(d.valor_hoja) : String(d.valor_hoja).replace('.', ',')) : String(d.valor_hoja);
      tr.append(name, el('td', null, d.campo), el('td', 'ep-num', vh), el('td', 'ep-num', d.valor_fuente), el('td', null, d.unidad || ''), res); return tr;
    }));
    const pend = rows('entidades').filter((e) => e.pendiente).sort((a, b) => VERS.indexOf(a.veredicto) - VERS.indexOf(b.veredicto) || a.nombre.localeCompare(b.nombre, 'es'));
    $('#tabla-pendientes tbody').replaceChildren(...pend.map((e) => { const tr = el('tr'); tr.dataset.key = String(e.id); const cv = el('td'); cv.appendChild(chip(e.veredicto));
      tr.append(el('td', 'ep-name', e.nombre), el('td', null, e.ccaa), cv, el('td', null, e.pendiente)); return tr; }));
  }

  // ---------- pages ----------
  const PAGES = ['resumen', 'duplicidades', 'entidades', 'personal', 'indicadores', 'verificacion'];
  function render() {
    const root = document.querySelector('.ep');
    fillMarks(root);
    if (['entidades', 'referencias_matriz', 'personal_desglose', 'csic_personal', 'verificacion_muestra', 'duplicidades', 'temas', 'gasto_capitulos'].every(ok)) {
      root.querySelectorAll('.dash-skeleton').forEach((n) => n.classList.remove('dash-skeleton'));
    }
    const p = state.page;
    if (p === 'resumen') drawResumen();
    if (p === 'duplicidades') { drawMatriz(); drawTemas(); }
    if (p === 'entidades') drawTabla();
    if (p === 'personal') { drawCsic(); drawDesglose(); }
    if (p === 'indicadores') drawInd();
    if (p === 'verificacion') drawVerif();
  }
  const pagePanels = () => document.querySelectorAll('section.ep-page');
  function show(page) {
    if (!PAGES.includes(page)) return;
    state.page = page;
    pagePanels().forEach((panel) => { panel.hidden = panel.id !== page; });
    PAGES.forEach((p) => { $('#tab-' + p).setAttribute('aria-selected', String(p === page)); });
    dash.setLink(page);
    render();
  }
  document.querySelectorAll('.ep-tab').forEach((b) => b.addEventListener('click', () => show(b.dataset.page)));
  $('#f-q').addEventListener('input', (ev) => { state.q = ev.target.value; drawTabla(); });
  [['#f-clase', 'clase'], ['#f-ver', 'ver'], ['#f-fun', 'fun'], ['#f-ambito', 'ambito'], ['#f-ccaa', 'ccaa']].forEach(([s, k]) => $(s).addEventListener('change', (ev) => { state[k] = ev.target.value; drawTabla(); }));
  $('#f-reset').addEventListener('click', () => { Object.assign(state, { q: '', clase: '', ver: '', fun: '', ambito: '', ccaa: '' }); ['#f-q', '#f-clase', '#f-ver', '#f-fun', '#f-ambito', '#f-ccaa'].forEach((s) => { $(s).value = ''; }); drawTabla(); });
  document.querySelectorAll('#tabla-entidades .ep-th-btn').forEach((b) => b.addEventListener('click', () => {
    const k = b.dataset.sort; if (state.sort === k) state.dir = -state.dir; else { state.sort = k; state.dir = typeof (rows('entidades')[0] || {})[k] === 'number' ? -1 : 1; }
    drawTabla();
  }));
  $('#tabla-entidades tbody').addEventListener('click', (ev) => {
    const tr = ev.target.closest('tr[data-key]'); if (!tr) return;
    const id = +tr.dataset.key; state.sel = state.sel === id ? null : id; drawTabla();
    if (state.sel) $('#detalle').scrollIntoView({ block: 'nearest' });
  });
  dash.onData(render);
  function routeFromHash() {
    const named = location.hash.slice(1);
    if (PAGES.includes(named)) show(named);
  }
  routeFromHash();
  window.addEventListener('hashchange', routeFromHash);
  let resizeT;
  window.addEventListener('resize', () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(render, 150);
  });
