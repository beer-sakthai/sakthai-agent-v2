# web/

A zero-build static dashboard: vanilla HTML + CSS + JS, hydrated from a JSON
snapshot the CLI exports. No framework, no bundler, no Vertex/Vercel coupling.

## Use

```bash
# 1. export a snapshot from your memory store
sakthai dashboard --export web/data.json

# 2. serve the folder (any static server)
python -m http.server -d web 8080
#    open http://localhost:8080
```

If `data.json` is missing (e.g. opened via `file://`), the page falls back to
the built-in demo sample so it still renders.

## Files

```
web/
├── index.html   # markup + view containers
├── styles.css   # styling
├── app.js       # fetches data.json and renders KPIs, growth, categories, tables
└── data.json    # snapshot from `sakthai dashboard --export` (git-ignored if you prefer)
```

The snapshot shape matches `sakthai/dashboard/data.py`
(`collect_dashboard_data`): `kpis`, `growth`, `categories`, `recent_facts`,
`top_observations`.
