import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"

with open(DATA_DIR / "books.json", encoding="utf-8") as f:
    rows = json.load(f)

cats = {}
for r in rows:
    cats[r["category"]] = cats.get(r["category"], 0) + 1
cat_list = sorted(cats.items(), key=lambda x: -x[1])

books_json = json.dumps(rows, ensure_ascii=False)
cats_json = json.dumps(cat_list, ensure_ascii=False)

html = f"""<title>書籍分析カタログ</title>
<style>
:root {{
  --bg: #EEECE3;
  --surface: #F8F6EF;
  --surface-alt: #F1EEE3;
  --ink: #2A2A22;
  --ink-soft: #6C6957;
  --ink-faint: #948F79;
  --line: #DAD5C4;
  --accent: #2E6B63;
  --accent-soft: #DCE9E5;
  --accent-ink: #1D453F;
  --chip-bg: #E4E0D0;
  --done-bg: #EAF1DA;
  --shadow: 0 1px 2px rgba(42,42,34,0.06), 0 4px 16px rgba(42,42,34,0.05);
  --radius: 10px;
  --font-serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Hiragino Mincho ProN", serif;
  --font-sans: "Avenir Next", "Helvetica Neue", "Hiragino Sans", "Yu Gothic", sans-serif;
  --font-mono: "SF Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #191A15;
    --surface: #212219;
    --surface-alt: #26271D;
    --ink: #ECE8DA;
    --ink-soft: #A9A38C;
    --ink-faint: #7C7863;
    --line: #34352A;
    --accent: #6FBFB0;
    --accent-soft: #22322E;
    --accent-ink: #A6E4D6;
    --chip-bg: #2C2D22;
    --done-bg: #26301F;
    --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.35);
  }}
}}
:root[data-theme="dark"] {{
  --bg: #191A15;
  --surface: #212219;
  --surface-alt: #26271D;
  --ink: #ECE8DA;
  --ink-soft: #A9A38C;
  --ink-faint: #7C7863;
  --line: #34352A;
  --accent: #6FBFB0;
  --accent-soft: #22322E;
  --accent-ink: #A6E4D6;
  --chip-bg: #2C2D22;
  --done-bg: #26301F;
  --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.35);
}}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 15px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}}

.wrap {{
  max-width: 1240px;
  margin: 0 auto;
  padding: 44px 28px 80px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}}

header.page {{
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-bottom: 1px solid var(--line);
  padding-bottom: 22px;
}}
.eyebrow {{
  font-family: var(--font-mono);
  font-size: 11.5px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
}}
h1 {{
  font-family: var(--font-serif);
  font-weight: 500;
  font-size: clamp(28px, 4vw, 38px);
  margin: 0;
  text-wrap: balance;
  color: var(--ink);
}}
.sub {{
  color: var(--ink-soft);
  font-size: 14.5px;
  max-width: 66ch;
}}

.progress-row {{
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
  flex-wrap: wrap;
}}
.progress-track {{
  flex: 1;
  min-width: 160px;
  max-width: 420px;
  height: 8px;
  border-radius: 999px;
  background: var(--chip-bg);
  overflow: hidden;
}}
.progress-fill {{
  height: 100%;
  background: var(--accent);
  border-radius: 999px;
  width: 0%;
  transition: width 0.3s ease;
}}
.progress-label {{
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 13px;
  color: var(--ink-soft);
  white-space: nowrap;
}}
.progress-label b {{ color: var(--ink); font-size: 15px; }}

.stats {{
  display: flex;
  gap: 22px;
  flex-wrap: wrap;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 13px;
  color: var(--ink-soft);
}}
.stats b {{
  color: var(--ink);
  font-size: 15px;
}}

.controls {{
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: sticky;
  top: 0;
  background: var(--bg);
  padding: 14px 0 16px;
  z-index: 5;
  border-bottom: 1px solid var(--line);
}}
.search-row {{
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}}
.search-row input[type="search"] {{
  flex: 1;
  min-width: 200px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 11px 14px;
  font-size: 14.5px;
  color: var(--ink);
  font-family: var(--font-sans);
}}
.search-row input[type="search"]:focus {{
  outline: 2px solid var(--accent);
  outline-offset: -1px;
}}
.sort-select, .btn {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 11px 12px;
  font-size: 13.5px;
  color: var(--ink);
  font-family: var(--font-sans);
}}
.btn {{
  cursor: pointer;
  white-space: nowrap;
}}
.btn:hover {{ border-color: var(--accent); color: var(--accent-ink); }}
.btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}
.status-msg {{
  font-size: 12px;
  color: var(--ink-faint);
  font-family: var(--font-mono);
}}

.chip-group {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}}
.chip-group-label {{
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-faint);
  margin-right: 2px;
}}
.chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}}
.chip {{
  border: 1px solid var(--line);
  background: var(--chip-bg);
  color: var(--ink-soft);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12.5px;
  font-family: var(--font-sans);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}}
.chip .n {{
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  color: var(--ink-faint);
  font-size: 11px;
}}
.chip:hover {{ border-color: var(--accent); color: var(--ink); }}
.chip.active {{
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}}
.chip.active .n {{ color: rgba(255,255,255,0.75); }}

.table-shell {{
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
}}
.table-scroll {{
  overflow-x: auto;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  min-width: 1080px;
}}
thead th {{
  text-align: left;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-faint);
  font-weight: 500;
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  background: var(--surface-alt);
  position: sticky;
  top: 0;
}}
tbody td {{
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}}
tbody tr:last-child td {{ border-bottom: none; }}
tbody tr:hover {{ background: var(--surface-alt); }}
tbody tr.row-done {{ background: var(--done-bg); }}
tbody tr.row-done:hover {{ background: var(--done-bg); filter: brightness(0.97); }}
.col-title {{ width: 17%; }}
.col-author {{ width: 12%; }}
.col-date {{ width: 8%; }}
.col-cat {{ width: 10%; }}
.col-summary {{ width: 33%; }}
.col-done {{ width: 8%; text-align: center; }}
.col-blogdate {{ width: 12%; }}

.title-cell {{
  font-family: var(--font-serif);
  font-size: 14.5px;
  color: var(--ink);
  line-height: 1.4;
}}
.author-cell {{ color: var(--ink-soft); font-size: 13px; }}
.date-cell {{
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 12.5px;
  color: var(--ink-soft);
  white-space: nowrap;
}}
.cat-cell .tag {{
  display: inline-block;
  font-size: 11.5px;
  padding: 3px 9px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-ink);
  white-space: nowrap;
}}
.summary-cell {{ color: var(--ink-soft); font-size: 13.3px; line-height: 1.6; }}

.done-cell {{ text-align: center; }}
.done-check {{
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
}}
.blogdate-cell input[type="date"] {{
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 5px 6px;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-size: 12px;
  color: var(--ink);
}}
.blogdate-cell input[type="date"]:disabled {{
  opacity: 0.45;
  background: transparent;
}}

.empty {{
  padding: 60px 20px;
  text-align: center;
  color: var(--ink-faint);
  font-family: var(--font-mono);
  font-size: 13px;
  display: none;
}}

footer.note {{
  color: var(--ink-faint);
  font-size: 12px;
  text-align: center;
  padding-top: 4px;
  line-height: 1.7;
}}

mark {{
  background: var(--accent-soft);
  color: var(--accent-ink);
  border-radius: 3px;
  padding: 0 1px;
}}

@media (max-width: 720px) {{
  .table-scroll {{ overflow-x: auto; }}
  table {{ min-width: 900px; }}
}}
</style>

<div class="wrap">
  <header class="page">
    <div class="eyebrow">01_Inbox / BookSummary</div>
    <h1>書籍分析カタログ</h1>
    <div class="sub">Obsidian vault 内の書籍分析ノートを一覧化。検索・分類フィルタ・ソートに加えて、ブログ化の進捗（作成済みチェックと作成日）を記録できます。</div>
    <div class="progress-row">
      <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label">ブログ化進捗　<b id="progress-count">0</b> / <span id="progress-total">283</span>（<b id="progress-pct">0</b>%）</div>
    </div>
    <div class="stats">
      <span><b id="stat-count">283</b> 件表示中</span>
      <span><b id="stat-cats">20</b> 分類</span>
    </div>
  </header>

  <div class="controls">
    <div class="search-row">
      <input type="search" id="search" placeholder="タイトル・著者・概要を検索…" autocomplete="off" />
      <select id="sort" class="sort-select">
        <option value="title">タイトル順</option>
        <option value="author">著者順</option>
        <option value="date">発行日順</option>
        <option value="category">分類順</option>
        <option value="blogdate">ブログ作成日順</option>
      </select>
      <button class="btn" id="btn-export" title="進捗をJSONファイルとして書き出し（バックアップ用）">進捗をエクスポート</button>
      <button class="btn" id="btn-import-trigger" title="エクスポートしたJSONを読み込んで復元">進捗をインポート</button>
      <input type="file" id="import-file" accept="application/json" style="display:none" />
      <span class="status-msg" id="status-msg"></span>
    </div>
    <div class="chip-group">
      <span class="chip-group-label">進捗</span>
      <div class="chips" id="status-chips"></div>
    </div>
    <div class="chip-group">
      <span class="chip-group-label">分類</span>
      <div class="chips" id="chips"></div>
    </div>
  </div>

  <div class="table-shell">
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th class="col-title">タイトル</th>
            <th class="col-author">著者</th>
            <th class="col-date">発行日</th>
            <th class="col-cat">分類</th>
            <th class="col-summary">概要</th>
            <th class="col-done">作成済</th>
            <th class="col-blogdate">作成日</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div class="empty" id="empty">該当する書籍が見つかりません</div>
  </div>

  <footer class="note">
    Obsidian vault「Helloworld / 01_Inbox / BookSummary」内の {len(rows)} 件のノートから自動集計<br />
    ブログ作成の進捗はこのブラウザ内（localStorage）に保存されます。他の端末・ブラウザとは同期されないため、定期的に「進捗をエクスポート」でバックアップしてください。
  </footer>
</div>

<script>
const BOOKS = {books_json};
const CATS = {cats_json};
const STORAGE_KEY = "bookCatalogProgress_v1";

function loadProgress() {{
  try {{
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{{}}");
  }} catch (e) {{
    return {{}};
  }}
}}
function saveProgress() {{
  try {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }} catch (e) {{ /* storage unavailable — state stays in-memory for this session */ }}
}}
function todayStr() {{
  return new Date().toISOString().slice(0, 10);
}}

let progress = loadProgress();
let state = {{ query: "", cat: null, status: null, sort: "title" }};

const chipsEl = document.getElementById("chips");
const statusChipsEl = document.getElementById("status-chips");
const tbody = document.getElementById("tbody");
const emptyEl = document.getElementById("empty");
const searchEl = document.getElementById("search");
const sortEl = document.getElementById("sort");
const statusMsgEl = document.getElementById("status-msg");

function escapeHtml(s) {{
  return String(s).replace(/[&<>"']/g, m => ({{
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }}[m]));
}}

function highlight(text, q) {{
  const safe = escapeHtml(text);
  if (!q) return safe;
  try {{
    const re = new RegExp(q.replace(/[.*+?^${{}}()|[\\]\\\\]/g, "\\\\$&"), "ig");
    return safe.replace(re, m => `<mark>${{m}}</mark>`);
  }} catch (e) {{ return safe; }}
}}

function parseDateKey(d) {{
  const m = (d || "").match(/(\\d{{4}})年?(\\d{{1,2}})?/);
  if (!m) return "0000-00";
  const y = m[1];
  const mo = (m[2] || "00").padStart(2, "0");
  return `${{y}}-${{mo}}`;
}}

function renderChips() {{
  const allChip = document.createElement("button");
  allChip.className = "chip" + (state.cat === null ? " active" : "");
  allChip.innerHTML = `すべて <span class="n">${{BOOKS.length}}</span>`;
  allChip.onclick = () => {{ state.cat = null; renderChips(); renderTable(); }};
  chipsEl.innerHTML = "";
  chipsEl.appendChild(allChip);
  for (const [cat, n] of CATS) {{
    const c = document.createElement("button");
    c.className = "chip" + (state.cat === cat ? " active" : "");
    c.innerHTML = `${{escapeHtml(cat)}} <span class="n">${{n}}</span>`;
    c.onclick = () => {{ state.cat = (state.cat === cat ? null : cat); renderChips(); renderTable(); }};
    chipsEl.appendChild(c);
  }}
}}

function renderStatusChips() {{
  const doneCount = BOOKS.filter(b => progress[b.id] && progress[b.id].done).length;
  const defs = [
    {{ key: null, label: "すべて", n: BOOKS.length }},
    {{ key: "pending", label: "未作成", n: BOOKS.length - doneCount }},
    {{ key: "done", label: "作成済み", n: doneCount }},
  ];
  statusChipsEl.innerHTML = "";
  for (const d of defs) {{
    const c = document.createElement("button");
    c.className = "chip" + (state.status === d.key ? " active" : "");
    c.innerHTML = `${{d.label}} <span class="n">${{d.n}}</span>`;
    c.onclick = () => {{ state.status = (state.status === d.key ? null : d.key); renderStatusChips(); renderTable(); }};
    statusChipsEl.appendChild(c);
  }}
}}

function updateProgressBar() {{
  const total = BOOKS.length;
  const done = BOOKS.filter(b => progress[b.id] && progress[b.id].done).length;
  const pct = total ? Math.round((done / total) * 100) : 0;
  document.getElementById("progress-count").textContent = done;
  document.getElementById("progress-total").textContent = total;
  document.getElementById("progress-pct").textContent = pct;
  document.getElementById("progress-fill").style.width = pct + "%";
}}

function renderTable() {{
  const q = state.query.trim().toLowerCase();
  let rows = BOOKS.filter(b => {{
    if (state.cat && b.category !== state.cat) return false;
    const rec = progress[b.id];
    const isDone = !!(rec && rec.done);
    if (state.status === "done" && !isDone) return false;
    if (state.status === "pending" && isDone) return false;
    if (!q) return true;
    return (b.title + " " + b.author + " " + b.summary + " " + b.category).toLowerCase().includes(q);
  }});

  rows = rows.slice().sort((a, b) => {{
    if (state.sort === "date") return parseDateKey(a.date).localeCompare(parseDateKey(b.date));
    if (state.sort === "author") return a.author.localeCompare(b.author, "ja");
    if (state.sort === "category") return a.category.localeCompare(b.category, "ja");
    if (state.sort === "blogdate") {{
      const da = (progress[a.id] && progress[a.id].date) || "";
      const db = (progress[b.id] && progress[b.id].date) || "";
      if (!da && !db) return a.title.localeCompare(b.title, "en");
      if (!da) return 1;
      if (!db) return -1;
      return da.localeCompare(db);
    }}
    return a.title.localeCompare(b.title, "en");
  }});

  document.getElementById("stat-count").textContent = rows.length;
  updateProgressBar();

  if (rows.length === 0) {{
    tbody.innerHTML = "";
    emptyEl.style.display = "block";
    return;
  }}
  emptyEl.style.display = "none";

  tbody.innerHTML = rows.map(b => {{
    const rec = progress[b.id] || {{}};
    const isDone = !!rec.done;
    const dateVal = rec.date || "";
    return `
    <tr class="${{isDone ? 'row-done' : ''}}">
      <td class="col-title title-cell">${{highlight(b.title, q)}}</td>
      <td class="col-author author-cell">${{highlight(b.author, q)}}</td>
      <td class="col-date date-cell">${{escapeHtml(b.date)}}</td>
      <td class="col-cat cat-cell"><span class="tag">${{escapeHtml(b.category)}}</span></td>
      <td class="col-summary summary-cell">${{highlight(b.summary, q)}}</td>
      <td class="col-done done-cell"><input type="checkbox" class="done-check" data-id="${{b.id}}" ${{isDone ? "checked" : ""}} /></td>
      <td class="col-blogdate blogdate-cell"><input type="date" class="done-date" data-id="${{b.id}}" value="${{escapeHtml(dateVal)}}" ${{isDone ? "" : "disabled"}} /></td>
    </tr>
  `;
  }}).join("");
}}

tbody.addEventListener("change", (e) => {{
  const id = e.target.getAttribute("data-id");
  if (id === null) return;
  const rec = progress[id] ? Object.assign({{}}, progress[id]) : {{}};
  if (e.target.classList.contains("done-check")) {{
    rec.done = e.target.checked;
    if (rec.done && !rec.date) rec.date = todayStr();
    progress[id] = rec;
    saveProgress();
    renderStatusChips();
    renderTable();
  }} else if (e.target.classList.contains("done-date")) {{
    rec.date = e.target.value;
    progress[id] = rec;
    saveProgress();
    updateProgressBar();
  }}
}});

searchEl.addEventListener("input", () => {{ state.query = searchEl.value; renderTable(); }});
sortEl.addEventListener("change", () => {{ state.sort = sortEl.value; renderTable(); }});

function showStatus(msg, ms) {{
  statusMsgEl.textContent = msg;
  if (ms) setTimeout(() => {{ if (statusMsgEl.textContent === msg) statusMsgEl.textContent = ""; }}, ms);
}}

let downloadsApi = null;
(async () => {{
  try {{
    downloadsApi = (typeof claude !== "undefined" && claude.use) ? await claude.use("downloads") : null;
  }} catch (e) {{
    downloadsApi = null;
  }}
  if (!downloadsApi) {{
    document.getElementById("btn-export").disabled = true;
    document.getElementById("btn-export").title = "この環境ではエクスポート機能が利用できません";
  }}
}})();

document.getElementById("btn-export").addEventListener("click", async () => {{
  if (!downloadsApi) return;
  const payload = {{
    exportedAt: new Date().toISOString(),
    totalBooks: BOOKS.length,
    progress: progress,
  }};
  try {{
    await downloadsApi.save({{
      filename: `book_catalog_progress_${{todayStr()}}.json`,
      data: JSON.stringify(payload, null, 2),
    }});
    showStatus("エクスポートしました", 3000);
  }} catch (err) {{
    if (err && err.code === "declined") {{
      showStatus("保存がキャンセルされました", 3000);
    }} else {{
      showStatus("エクスポートに失敗しました", 3000);
    }}
  }}
}});

document.getElementById("btn-import-trigger").addEventListener("click", () => {{
  document.getElementById("import-file").click();
}});
document.getElementById("import-file").addEventListener("change", (e) => {{
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {{
    try {{
      const parsed = JSON.parse(reader.result);
      const incoming = (parsed && typeof parsed === "object" && parsed.progress) ? parsed.progress : parsed;
      progress = Object.assign({{}}, progress, incoming);
      saveProgress();
      renderStatusChips();
      renderTable();
      showStatus("進捗を読み込みました", 3000);
    }} catch (err) {{
      showStatus("読み込みに失敗しました（JSON形式を確認してください）", 4000);
    }}
  }};
  reader.readAsText(file);
  e.target.value = "";
}});

document.getElementById("stat-cats").textContent = CATS.length;
renderChips();
renderStatusChips();
renderTable();
</script>
"""

DIST_DIR.mkdir(exist_ok=True)
out_path = DIST_DIR / "book_catalog.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", out_path, len(html), "chars")
