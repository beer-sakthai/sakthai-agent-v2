"use strict";

// Built-in fallback so the page renders even without a data.json (e.g. file://).
const DEMO = {
  source: "demo",
  generated_at: "demo",
  kpis: { total_facts: 5, total_facts_delta: 5, total_observations: 2, total_observations_delta: 2 },
  growth: {
    labels: ["1", "2", "3", "4", "5", "6", "7"],
    facts: [1, 2, 2, 3, 4, 4, 5],
    observations: [0, 0, 1, 1, 1, 2, 2],
  },
  categories: [
    { name: "Pref", count: 2, color: "#a855f7" },
    { name: "Profile", count: 1, color: "#34d399" },
    { name: "Note", count: 1, color: "#3b82f6" },
    { name: "Observations", count: 2, color: "#f472b6" },
  ],
  recent_facts: [
    { id: 5, kind: "pref", key: "language", value: "Python" },
    { id: 4, kind: "pref", key: "editor", value: "VS Code" },
  ],
  top_observations: [{ summary: "Prefers concise replies", weight: 0.9 }],
};

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderKpis(kpis) {
  const root = document.getElementById("kpis");
  root.innerHTML = "";
  const items = [
    { label: "Facts", value: kpis.total_facts, delta: kpis.total_facts_delta },
    { label: "Observations", value: kpis.total_observations, delta: kpis.total_observations_delta },
  ];
  for (const it of items) {
    const card = el("div", "kpi");
    card.appendChild(el("div", "value", it.value));
    card.appendChild(el("div", "label", it.label));
    card.appendChild(el("div", "delta", `+${it.delta} this week`));
    root.appendChild(card);
  }
}

function renderGrowth(growth) {
  const canvas = document.getElementById("growth");
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height, pad = 24;
  ctx.clearRect(0, 0, w, h);
  const series = [
    { data: growth.facts, color: "#3b82f6" },
    { data: growth.observations, color: "#f472b6" },
  ];
  const max = Math.max(1, ...growth.facts, ...growth.observations);
  const n = growth.labels.length || 1;
  const x = (i) => pad + (i * (w - 2 * pad)) / Math.max(1, n - 1);
  const y = (v) => h - pad - (v * (h - 2 * pad)) / max;
  for (const s of series) {
    ctx.strokeStyle = s.color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    s.data.forEach((v, i) => (i ? ctx.lineTo(x(i), y(v)) : ctx.moveTo(x(i), y(v))));
    ctx.stroke();
  }
}

function renderCategories(categories) {
  const root = document.getElementById("categories");
  root.innerHTML = "";
  const max = Math.max(1, ...categories.map((c) => c.count));
  for (const c of categories) {
    const row = el("div", "bar-row");
    row.appendChild(el("span", "name", c.name));
    const track = el("div", "track");
    const fill = el("div", "fill");
    fill.style.width = `${(c.count / max) * 100}%`;
    fill.style.background = c.color;
    track.appendChild(fill);
    row.appendChild(track);
    row.appendChild(el("span", "count", String(c.count)));
    root.appendChild(row);
  }
}

function renderFacts(facts) {
  const body = document.querySelector("#facts tbody");
  body.innerHTML = "";
  for (const f of facts) {
    const tr = el("tr");
    tr.appendChild(el("td", "kind", `[${f.kind}]`));
    tr.appendChild(el("td", "value", f.key ? `${f.key}: ${f.value}` : f.value));
    body.appendChild(tr);
  }
}

function renderObservations(observations) {
  const body = document.querySelector("#observations tbody");
  body.innerHTML = "";
  for (const o of observations) {
    const tr = el("tr");
    tr.appendChild(el("td", "weight", o.weight.toFixed(2)));
    tr.appendChild(el("td", "summary", o.summary));
    body.appendChild(tr);
  }
}

function render(data) {
  const src = document.getElementById("source");
  src.textContent =
    data.source === "live" ? `Live data · generated ${data.generated_at}` : "Demo data — memory is empty.";
  renderKpis(data.kpis);
  renderGrowth(data.growth);
  renderCategories(data.categories);
  renderFacts(data.recent_facts);
  renderObservations(data.top_observations);
}

fetch("data.json")
  .then((r) => (r.ok ? r.json() : Promise.reject()))
  .then(render)
  .catch(() => render(DEMO));
