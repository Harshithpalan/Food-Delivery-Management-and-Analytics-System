"""
foodos_theme.py  -  drop-in modern, animated theme for the FoodOS Streamlit app.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;600&display=swap');

:root{
  --ink:#0E1518;        /* night-market teal-black */
  --panel:#162126;
  --panel-2:#1D2C32;
  --line:rgba(244,239,230,.10);
  --text:#F4EFE6;       /* steamed-rice white */
  --muted:#9FB0B3;
  --saffron:#FFB627;
  --chili:#FF5A45;
  --pistachio:#7BD389;
}

html, body, [class*="css"], .stApp { font-family:'DM Sans',sans-serif; color:var(--text); }
h1,h2,h3,h4 { font-family:'Bricolage Grotesque',sans-serif !important; letter-spacing:-.02em; color:var(--text) !important; }

/* ---------- background: slow drifting glow ---------- */
.stApp{
  background:
    radial-gradient(1200px 800px at 15% -10%, rgba(255,182,39,.35), transparent 70%),
    radial-gradient(1000px 800px at 100% 10%, rgba(255,90,69,.30), transparent 70%),
    radial-gradient(800px 600px at 50% 100%, rgba(123,211,137,.20), transparent 60%),
    var(--ink);
  background-size:140% 140%, 140% 140%, 140% 140%, auto;
  animation:drift 20s ease-in-out infinite alternate;
}
@keyframes drift{ from{background-position:0% 0%,100% 0%,0 0} to{background-position:8% 6%,92% 8%,0 0} }

header[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:2.5rem; max-width:1200px; }
hr{ border-color:var(--line) !important; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#121C21 0%,#0C1215 100%);
  border-right:1px solid var(--line);
}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{
  background:linear-gradient(90deg,var(--saffron),var(--chili));
  -webkit-background-clip:text; background-clip:text; color:transparent !important;
  font-weight:800;
}
/* nav radio -> pills */
[data-testid="stSidebar"] div[role="radiogroup"]{ gap:.35rem; }
[data-testid="stSidebar"] div[role="radiogroup"] label{
  padding:.65rem .9rem; border-radius:12px; width:100%;
  border:1px solid transparent; cursor:pointer;
  transition:background .25s, transform .25s, border-color .25s;
}
[data-testid="stSidebar"] div[role="radiogroup"] label p { color: var(--text) !important; }
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child{ display:none; }
[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
  background:var(--panel-2); transform:translateX(4px);
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
  background:linear-gradient(90deg,rgba(255,182,39,.30),rgba(255,90,69,.15));
  border-color:rgba(255,182,39,.60);
  box-shadow:inset 4px 0 0 var(--saffron), 0 0 15px rgba(255,182,39,.3);
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{ color:var(--saffron); font-weight:600; text-shadow: 0 0 8px rgba(255,182,39,.5); }

/* ---------- KPI cards (custom) ---------- */
@property --n { syntax:'<integer>'; initial-value:0; inherits:false; }
.kpi-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1.1rem; margin:1.2rem 0 2rem; }
.kpi{
  position:relative; overflow:hidden; padding:1.3rem 1.4rem; border-radius:18px;
  background:linear-gradient(160deg,var(--panel-2),var(--panel));
  border:1px solid var(--line);
  box-shadow: 0 4px 20px rgba(0,0,0,.4);
  transition:transform .3s ease, border-color .3s ease, box-shadow .3s ease;
}
.kpi::before{ /* accent bar */
  content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--accent,var(--saffron));
  box-shadow: 0 0 10px var(--accent,var(--saffron));
}
.kpi::after{ /* one-time light sweep on load */
  content:""; position:absolute; inset:0; transform:translateX(-120%);
  background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.15) 50%,transparent 70%);
  animation:sweep 1.6s .4s ease-out 1 forwards;
}
@keyframes sweep{ to{ transform:translateX(120%);} }
.kpi:hover{ transform:translateY(-4px); border-color:var(--accent,var(--saffron)); box-shadow:0 0 25px var(--accent,var(--saffron)); }
.kpi .icon{ font-size:1.4rem; }
.kpi .label{ color:var(--muted); font-size:.92rem; margin-top:.35rem; }
.kpi .value{
  font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:2.6rem; line-height:1.1; margin-top:.15rem;
}
.kpi .count{ animation:count 1.4s cubic-bezier(.2,.8,.2,1) forwards; counter-reset:n var(--n); }
.kpi .count::after{ content:counter(n); }
@keyframes count{ from{--n:0} to{--n:var(--to)} }
.kpi .value.pop{ animation:pop .9s cubic-bezier(.2,.8,.2,1) both; }
@keyframes pop{ from{opacity:0; filter:blur(6px); transform:translateY(8px)} to{opacity:1; filter:none; transform:none} }

/* ---------- page header ---------- */
.page-head h1{ font-size:3rem; font-weight:800; margin:0; }
.page-head h1 span{ background:linear-gradient(90deg,var(--saffron),var(--chili)); -webkit-background-clip:text; background-clip:text; color:transparent; }
.page-head p{ color:var(--muted); font-size:1.05rem; margin:.4rem 0 0; }
.live{ display:inline-flex; align-items:center; gap:.5rem; margin-top:1rem; padding:.3rem .8rem;
  border-radius:999px; border:1px solid var(--line); color:var(--pistachio); font-size:.85rem; background:rgba(123,211,137,.08); }
.live i{ width:8px; height:8px; border-radius:50%; background:var(--pistachio); animation:pulse 1.8s infinite; }
@keyframes pulse{ 0%{box-shadow:0 0 0 0 rgba(123,211,137,.6)} 100%{box-shadow:0 0 0 10px rgba(123,211,137,0)} }

/* ---------- native widgets ---------- */
[data-testid="stMetric"]{ background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:1rem 1.2rem; }
.stButton>button, .stDownloadButton>button{
  border-radius:12px; border:1px solid rgba(255,182,39,.5); color:var(--ink); font-weight:600;
  background:linear-gradient(90deg,var(--saffron),#FF9A3C);
  transition:transform .2s, box-shadow .2s;
}
.stButton>button:hover{ transform:translateY(-2px); box-shadow:0 10px 22px -8px rgba(255,182,39,.55); color:var(--ink); border-color:var(--saffron); }
.stButton>button:active{ transform:scale(.97); }
[data-testid="stExpander"]{ background:var(--panel); border:1px solid var(--line) !important; border-radius:14px; }
[data-testid="stExpander"] summary:hover{ color:var(--saffron); }
[data-testid="stDataFrame"]{ border:1px solid var(--line); border-radius:14px; overflow:hidden; }
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div,.stNumberInput input{
  background:var(--panel) !important; border-radius:12px !important; border:1px solid var(--line) !important;
  color: var(--text) !important;
  transition:border-color .2s, box-shadow .2s;
}
label, .st-emotion-cache-10trnc2 { color: var(--text) !important; }
.stTextInput input:focus{ border-color:var(--saffron) !important; box-shadow:0 0 0 3px rgba(255,182,39,.2) !important; }
button[role="tab"][aria-selected="true"]{ color:var(--saffron) !important; }
div[data-baseweb="tab-highlight"]{ background:var(--saffron) !important; }

/* ---------- respect reduced motion ---------- */
@media (prefers-reduced-motion:reduce){
  .stApp,.kpi::after,.kpi .value,.live i{ animation:none !important; }
  .kpi .count{ --n:var(--to); counter-reset:n var(--to); }
}
</style>
"""

def inject_theme():
    """Call once per run, right after st.set_page_config()."""
    st.markdown(CSS, unsafe_allow_html=True)

def page_header(title_plain, title_accent="", subtitle="", live=True):
    badge = '<div class="live"><i></i>Live database connection</div>' if live else ""
    st.markdown(
        f'<div class="page-head"><h1>{title_plain} <span>{title_accent}</span></h1>'
        f"<p>{subtitle}</p>{badge}</div>",
        unsafe_allow_html=True,
    )

def kpi_row(items):
    cards = []
    for it in items:
        v, pre, suf = it["value"], it.get("prefix", ""), it.get("suffix", "")
        accent = it.get("accent", "#FFB627")
        if isinstance(v, int):
            html_val = (f'<div class="value">{pre}<span class="count" style="--to:{v}"></span>{suf}</div>')
        else:
            shown = f"{v:,.2f}" if isinstance(v, float) else str(v)
            html_val = f'<div class="value pop">{pre}{shown}{suf}</div>'
        cards.append(
            f'<div class="kpi" style="--accent:{accent}">'
            f'<div class="icon">{it.get("icon","")}</div>'
            f'<div class="label">{it["label"]}</div>{html_val}</div>'
        )
    st.markdown(f'<div class="kpi-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

def section(icon, title):
    st.markdown(f"### {icon} {title}")
