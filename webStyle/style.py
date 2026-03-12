import streamlit as st

# CSS 
MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; }

section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0D2137 0%, #1B4F72 60%, #2874A6 100%);
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #0D1B2A; border-radius: 14px;
    padding: 6px 10px; border: 1px solid rgba(255,255,255,0.08); flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px;
    color: rgba(255,255,255,0.6) !important;
    font-family: 'Tajawal', sans-serif; font-weight: 600;
    font-size: 0.88rem; padding: 8px 18px; border: none !important; transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1B4F72, #2874A6) !important;
    color: #fff !important; box-shadow: 0 3px 12px rgba(40,116,166,0.45);
}
.stTabs [data-baseweb="tab"]:hover { background: rgba(255,255,255,0.08) !important; color: #fff !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }

.hero {
    background: linear-gradient(135deg, #0D2137 0%, #1B4F72 50%, #2874A6 100%);
    border-radius: 16px; padding: 36px 48px; margin-bottom: 28px;
    box-shadow: 0 8px 40px rgba(27,79,114,0.35); position: relative; overflow: hidden;
}
.hero::after {
    content:''; position:absolute; bottom:-70px; right:-50px;
    width:300px; height:300px; border-radius:50%; background:rgba(212,172,13,0.07);
}
.hero-badge {
    display:inline-block; background:rgba(212,172,13,0.22);
    border:1px solid rgba(212,172,13,0.5); color:#F4D03F;
    font-size:0.75rem; font-weight:600; padding:4px 14px; border-radius:50px; margin-bottom:10px;
    font-family:'IBM Plex Mono',monospace; letter-spacing:.05em;
}
.hero-title { font-size:2.2rem; font-weight:800; color:#fff; margin:0 0 6px; }
.hero-sub   { font-size:0.98rem; color:rgba(255,255,255,.72); margin:0; }

.kpi {
    background:#fff; border-radius:14px; padding:20px 16px 16px;
    box-shadow:0 2px 16px rgba(27,79,114,.09); border-top:4px solid #2E86C1; text-align:center;
}
.kpi.red  { border-top-color:#C0392B; }
.kpi.gold { border-top-color:#D4AC0D; }
.kpi-val  { font-size:1.85rem; font-weight:800; color:#1B4F72; font-family:'IBM Plex Mono',monospace; line-height:1.1; }
.kpi-delta { font-size:0.85rem; font-weight:700; margin-top:3px; }
.kpi-delta.up   { color:#1E8449; }
.kpi-delta.down { color:#C0392B; }
.kpi-label { font-size:0.78rem; color:#717D7E; margin-top:4px; }

.sec { display:flex; align-items:center; gap:12px; margin:32px 0 14px; }
.sec-line { flex:1; height:2px; background:linear-gradient(90deg,#2E86C1,transparent); }
.sec-title { font-size:1.15rem; font-weight:700; color:#1B4F72; white-space:nowrap; }

.desc {
    background:linear-gradient(135deg,#EBF5FB,#FDFEFE); border:1px solid #AED6F1;
    border-radius:14px; padding:22px 28px; margin-bottom:20px;
}
.desc p { color:#1C2833; line-height:1.85; font-size:.93rem; margin:0 0 8px; }
.desc p:last-of-type { margin:0; }
.tags { display:flex; flex-wrap:wrap; gap:7px; margin-top:12px; }
.tag { background:rgba(27,79,114,.1); color:#1B4F72; border-radius:50px; padding:3px 12px; font-size:.75rem; font-weight:600; }

.insight-card {
    background: linear-gradient(135deg, #0D1F33 0%, #112233 100%);
    border: 1px solid rgba(46,134,193,0.35); border-right: 4px solid #2E86C1;
    border-radius: 12px; padding: 18px 24px; margin-top: 10px; margin-bottom: 28px;
}
.insight-card .insight-title {
    font-size: 0.82rem; font-weight: 700; color: #5DADE2;
    letter-spacing: 0.06em; margin-bottom: 10px;
    font-family: 'IBM Plex Mono', monospace;
}
.insight-card ul { margin: 0; padding-right: 20px; list-style: none; }
.insight-card ul li {
    color: #D6EAF8; font-size: 0.90rem; line-height: 1.85; margin-bottom: 4px; padding-right: 4px;
}
.insight-card ul li::before { content: "◆ "; color: #2E86C1; font-size: 0.65rem; vertical-align: middle; margin-left: 4px; }
.insight-card .highlight-up   { color: #2ECC71; font-weight: 700; }
.insight-card .highlight-down { color: #E74C3C; font-weight: 700; }
.insight-card .highlight-gold { color: #F4D03F; font-weight: 700; }

#MainMenu, footer, header { visibility:hidden; }
.block-container { padding-top:1.5rem; padding-bottom:3rem; }
</style>
"""
def inject_css():
    st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def insight(title, bullets):
    items = "".join(f"<li>{b}</li>" for b in bullets)
    st.markdown(f"""
    <div class="insight-card">
      <div class="insight-title">💡 {title}</div>
      <ul>{items}</ul>
    </div>""", unsafe_allow_html=True)

def pct(val, total):
    return round(val / total * 100, 1) if total else 0

YEARS = [2021, 2022, 2023]
YC    = {2021: "#2874A6", 2022: "#1E8449", 2023: "#E67E22"}

DARK_BG    = "#0A0F1E"
DARK_PAPER = "#0D1526"
DARK_GRID  = "rgba(255,255,255,0.07)"
DARK_AXIS  = "rgba(255,255,255,0.35)"
DARK_TEXT  = "#E8EDF5"
FONT       = "Tajawal"

def dark_layout(fig, title, h=400, ml=40, mr=30, mt=55, mb=20):
    fig.update_layout(
        title=title, title_x=0.5, title_font_size=15, title_font_color=DARK_TEXT,
        font_family=FONT, font_color=DARK_TEXT,
        plot_bgcolor=DARK_BG, paper_bgcolor=DARK_PAPER,
        height=h, margin=dict(l=ml, r=mr, t=mt, b=mb),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font_color=DARK_TEXT, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, zerolinecolor=DARK_GRID),
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, zerolinecolor=DARK_GRID),
    )
    return fig