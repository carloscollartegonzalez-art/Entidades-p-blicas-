"""Builds the dashboard page from its parts.

Writes two files in dashboard/:
- index.html: the page as published in the Claude "Dashboard" artifact (style + markup + calculations + drawing code).
  The artifact runtime provides the `dash` object, the CSS tokens and d3; the datasets are uploaded separately.
- preview.html: a standalone copy that opens in any browser without Claude. It inlines the datasets from
  dashboard/datos/, loads d3 from dashboard/vendor/d3.min.js and adds a minimal `dash` stand-in and fallback CSS tokens.
  It is for checking content, not a pixel-exact copy of the published dashboard.

Usage: python3 scripts/build_dashboard.py
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
D = BASE / 'dashboard'
ENC = 'utf-8'
DATASETS = ['entidades', 'referencias_matriz', 'personal_desglose', 'csic_personal', 'verificacion_muestra',
            'gasto_capitulos', 'duplicidades', 'temas']
D3 = D / 'vendor' / 'd3.min.js'

style = (D / 'style.css').read_text(encoding=ENC)
body = (D / 'body.html').read_text(encoding=ENC)
calcs = (D / 'calcs.js').read_text(encoding=ENC)
app = (D / 'app.js').read_text(encoding=ENC)

page = f"{style}{body}<script>\n{calcs}</script>\n<script>\n{app}</script>\n"
(D / 'index.html').write_text(page, encoding=ENC)

data = {n: json.loads((D / 'datos' / f'{n}.json').read_text(encoding=ENC)) for n in DATASETS}

TOKENS = """<style>
:root {
  --font-anthropic-sans: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-anthropic-serif: Georgia, 'Times New Roman', serif;
  --color-bg: #faf9f6; --color-panel: #ffffff; --color-fg: #1f1e1c; --color-fg-muted: #6b6862;
  --color-border-line: #e3e0d8; --color-ok: #2e7d4f; --color-warn: #b7791f; --color-bad: #c0392b;
  --cds-chart-muted: #a9a59c; --cds-chart-status-critical: #c0392b; --cds-chart-reference: #8a867d;
  --cds-text-secondary: #6b6862; --cds-surface-popover: #ffffff; --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.12);
  --cds-border: 1px solid #e3e0d8; --cds-radius: 10px;
  --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 16px; --cds-gap-lg: 24px;
  --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-md: 16px; --cds-pad-lg: 24px;
  --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 18px; --cds-font-size-title: 26px;
  --cds-font-weight-medium: 600; --cds-dur-slow: .3s; --cds-ease-out: ease-out;
}
@media (prefers-color-scheme: dark) {
  :root { --color-bg: #1c1b19; --color-panel: #262522; --color-fg: #f1efe9; --color-fg-muted: #a8a49b;
          --color-border-line: #3a3833; --cds-surface-popover: #2e2c29; --cds-border: 1px solid #3a3833; }
}
body { margin: 0; padding: 16px; background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); }
.ep-card, .ep-kpi { background: var(--color-panel); border: var(--cds-border); border-radius: var(--cds-radius); padding: var(--cds-pad-md); }
.dash-skeleton { opacity: .5; }
</style>"""

STUB = """<script>
window.__DATA = %s;
(function () {
  const calcs = {}; const cache = {};
  window.dash = {
    colors: ['#3266ad', '#2e9e7a', '#d08c2c', '#8a5cc2', '#c4466a', '#6b6862'],
    calc: (id, o) => { calcs[id] = o; },
    data: (id) => {
      if (cache[id]) return cache[id];
      if (window.__DATA[id]) return (cache[id] = { status: 'ok', data: window.__DATA[id] });
      const o = calcs[id]; if (!o) return { status: 'error' };
      return (cache[id] = { status: 'ok', data: o.fn(...o.inputs.map((i) => dash.data(i).data)) });
    },
    onData: (f) => { setTimeout(f, 0); },
    setLink: (page) => { history.replaceState(null, '', '#' + page); },
  };
})();
</script>""" % json.dumps(data, ensure_ascii=False)

if not D3.is_file():
    raise SystemExit(f'Missing {D3.relative_to(BASE)} — run: curl -o dashboard/vendor/d3.min.js '
                     'https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js')

preview = ("<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\">"
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
           "<title>Entidades públicas: vista previa</title>"
           "<script src=\"vendor/d3.min.js\"></script>"
           f"{TOKENS}{STUB}</head><body><div id=\"dash-root\">{page}</div></body></html>")
(D / 'preview.html').write_text(preview, encoding=ENC)
print('dashboard/index.html', len(page), '| dashboard/preview.html', len(preview))
