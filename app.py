import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Smurfit Westrock ESG Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F0F4F8; }
.dashboard-header {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B3A5C 100%);
    border-radius: 12px; padding: 24px 32px; margin-bottom: 20px;
    display: flex; justify-content: space-between; align-items: center;
}
.header-left h1 { color: #FFFFFF; font-size: 26px; font-weight: 800; margin: 0 0 4px 0; }
.header-left p  { color: #A8C4E0; font-size: 12px; margin: 0; }
.header-badge {
    background: #1E88E5; color: white; padding: 10px 20px;
    border-radius: 8px; font-size: 13px; font-weight: 600; text-align: right;
}
.header-badge span { display: block; font-size: 10px; opacity: 0.85; margin-bottom: 2px; }
.kpi-card {
    background: white; border-radius: 10px; padding: 16px 18px;
    border-left: 4px solid #1E88E5; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.kpi-label {
    font-size: 10px; font-weight: 600; color: #1E88E5; text-transform: uppercase;
    background: #EBF5FB; display: inline-block; padding: 2px 8px;
    border-radius: 4px; margin-bottom: 6px;
}
.kpi-title { font-size: 12px; color: #5A6A7A; margin-bottom: 4px; font-weight: 500; }
.kpi-value { font-size: 24px; font-weight: 800; color: #0D1B2A; margin-bottom: 2px; }
.kpi-sub   { font-size: 10px; color: #8A9BAB; }
.section-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 14px;
}
.section-title { font-size: 14px; font-weight: 700; color: #0D1B2A; margin-bottom: 2px; }
.section-sub   { font-size: 11px; color: #8A9BAB; margin-bottom: 10px; }
.data-note {
    background: #FFF8E1; border-left: 4px solid #FFC107; border-radius: 6px;
    padding: 10px 16px; font-size: 12px; color: #795548; margin-bottom: 16px;
}
.highlight-item {
    display: flex; align-items: flex-start; gap: 8px;
    margin-bottom: 10px; font-size: 12px; color: #2C3E50; line-height: 1.5;
}
.highlight-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #1E88E5; margin-top: 4px; flex-shrink: 0;
}
.footer {
    text-align: center; font-size: 11px; color: #AAB8C2;
    padding: 16px 0 8px; border-top: 1px solid #E8EDF2; margin-top: 8px;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 20px !important; padding-bottom: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
YEARS = [2020, 2021, 2022, 2023, 2024]
sk_scope1   = [2545, 2500, 2541, 2415, 2473]
sk_scope2   = [566,  553,  508,  467,  479]
sk_scope12  = [s1+s2 for s1, s2 in zip(sk_scope1, sk_scope2)]
sk_water    = [144.3, 140.1, 141.1, 131.7, 128.9]
sk_landfill = [442038, 426106, 452757, 370935, 313508]
sk_recovery = [405801, 475022, 488476, 478944, 516174]
sk_other    = [9022,  14129,  14566,  17336,  23786]
sk_certwood = [57.3, 56.2, 56.9, 56.8, 58.6]
sk_recycled = [75.4, 75.6, 76.2, 76.5, 76.4]
wrk_scope3_labels = ["Cat 1\nPurch. Goods","Cat 3\nFuel & Energy","Cat 10\nProcessing","Cat 12\nEnd-of-Life","Cat 9\nTransport"]
wrk_scope3_vals   = [2333, 2131, 444, 3172, 116]
mat_topics = [
    ("Climate Change",10.2,10.0,220),("Waste & Circular Econ.",10.0,9.1,180),
    ("Forest (Sust. Sourcing)",9.5,9.2,160),("Supply Chain Sust.",8.5,9.0,140),
    ("Water Management",8.2,8.5,120),("Energy Efficiency",9.0,8.4,120),
    ("Community Engagement",7.2,8.0,100),("Health & Safety",9.2,7.2,100),
    ("Biodiversity",7.0,7.0,90),
]
C = dict(navy="#0D1B2A",blue="#1E88E5",teal="#00ACC1",green="#43A047",amber="#FFA000",red="#E53935")

def fig_style(fig, ax):
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color("#E0E6EE")
    ax.tick_params(colors="#8A9BAB", labelsize=8)
    ax.yaxis.label.set_color("#8A9BAB"); ax.yaxis.label.set_size(8)
    ax.grid(axis="y", color="#F0F4F8", linewidth=0.8)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
  <div class="header-left">
    <h1>🌿 Smurfit Westrock ESG Performance Dashboard</h1>
    <p>Environmental metrics, material issues, and progress toward targets &nbsp;|&nbsp; Legacy-company data, 2024 focus</p>
  </div>
  <div class="header-badge"><span>2024 FOCUS</span>Merger Transition</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="data-note">
  ⚠️ <strong>Merger context:</strong> Smurfit WestRock was formed mid-2024.
  Trend data is <em>legacy Smurfit Kappa (SK)</em>; 2024 snapshot KPIs for WestRock (WRK) reported separately.
  Consolidated targets still in development as of 2025.
</div>""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
kpis = [
    ("SK Scope 1 (2024)",   "2,473 kt CO₂",  "Climate",      "YoY: −2.8% | Trend: ↓ since 2021"),
    ("SK Scope 1+2 (2024)", "2,952 kt CO₂",  "Climate",      "Combined; legacy Smurfit Kappa"),
    ("WRK Scope 1+2",       "7,974 kt CO₂e", "Climate",      "Legacy WestRock 2024 assured"),
    ("SK Water (2024)",     "128.9 Mm³",      "Water",        "YoY: −2.1% | Best in 5-yr series"),
    ("SK Cert. Wood",       "58.6%",          "Forest/Fiber", "YoY: +1.8pp | 5-yr high"),
    ("WRK Renewable Mix",   "60%",            "Energy",       "Legacy WestRock 2024 energy"),
]
for col, (title, value, label, sub) in zip(st.columns(6), kpis):
    with col:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: GHG Trend + Materiality ───────────────────────────────────────────
col_ghg, col_mat = st.columns([1.1, 0.9])

with col_ghg:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Climate Progress — Scope 1 & 2 Trend (SK Legacy, 2020–2024)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Legacy Smurfit Kappa direct and indirect emissions</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(YEARS, sk_scope1,  marker="o", color=C["blue"],  lw=2, ms=6, label="Scope 1")
    ax.plot(YEARS, sk_scope2,  marker="o", color=C["green"], lw=2, ms=6, label="Scope 2")
    ax.plot(YEARS, sk_scope12, marker="o", color=C["red"],   lw=2, ms=6, label="Scope 1+2", ls="--")
    ax.set_ylabel("ktonnes CO₂"); ax.set_xticks(YEARS)
    ax.legend(fontsize=8, frameon=False)
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_mat:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Materiality Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Business impact vs. stakeholder importance</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5.5, 3))
    for name, biz, stake, sz in mat_topics:
        ax.scatter(biz, stake, s=sz, color=C["blue"], alpha=0.65, zorder=3)
        ax.annotate(name, (biz, stake), fontsize=6.2, color="#2C3E50",
                    xytext=(4,4), textcoords="offset points")
    ax.axhline(8.5, color="#CCCCCC", ls="--", lw=0.8)
    ax.axvline(8.5, color="#CCCCCC", ls="--", lw=0.8)
    ax.set_xlabel("Business Impact", fontsize=8, color="#8A9BAB")
    ax.set_ylabel("Stakeholder Importance", fontsize=8, color="#8A9BAB")
    ax.set_xlim(6.2, 11); ax.set_ylim(6.2, 11)
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2: Water, Waste, Scope 3, Highlights ─────────────────────────────────
col_w, col_ws, col_s3, col_hi = st.columns([0.85, 1.1, 1.05, 0.95])

with col_w:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💧 Water Withdrawal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">SK Legacy 2020–2024 (Mm³)</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.plot(YEARS, sk_water, marker="o", color=C["teal"], lw=2, ms=6)
    ax.fill_between(YEARS, sk_water, alpha=0.08, color=C["teal"])
    for x, y in zip(YEARS, sk_water):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0,6),
                    ha="center", fontsize=7, color="#5A6A7A")
    ax.set_ylabel("Mm³"); ax.set_xticks(YEARS); ax.set_ylim(120, 152)
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_ws:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">♻️ Waste Pathways</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">SK Legacy non-hazardous waste (tonnes)</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 2.6))
    x = np.arange(len(YEARS)); w = 0.55
    rec = np.array(sk_recovery); lan = np.array(sk_landfill); oth = np.array(sk_other)
    ax.bar(x, rec, w, label="Recovery", color=C["green"], alpha=0.85)
    ax.bar(x, lan, w, bottom=rec, label="Landfill", color=C["red"], alpha=0.75)
    ax.bar(x, oth, w, bottom=rec+lan, label="Other", color=C["amber"], alpha=0.75)
    ax.set_xticks(x); ax.set_xticklabels(YEARS)
    ax.legend(fontsize=7, frameon=False, ncol=3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v/1e3:.0f}k"))
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔗 WestRock Scope 3 Hotspots</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">2024 value-chain emissions (kt CO₂e)</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4.5, 2.6))
    bar_colors = [C["blue"], C["teal"], C["green"], C["red"], C["amber"]]
    bars = ax.barh(wrk_scope3_labels, wrk_scope3_vals, color=bar_colors, alpha=0.85)
    for bar, val in zip(bars, wrk_scope3_vals):
        ax.text(bar.get_width()+40, bar.get_y()+bar.get_height()/2,
                f"{val:,}", va="center", fontsize=7.5, color="#5A6A7A")
    ax.set_xlabel("kt CO₂e", fontsize=8, color="#8A9BAB")
    ax.invert_yaxis()
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color("#E0E6EE")
    ax.tick_params(colors="#8A9BAB", labelsize=8)
    ax.grid(axis="x", color="#F0F4F8", lw=0.8)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_hi:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⭐ Strategic Highlights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Best-performing signals, 2024</div>', unsafe_allow_html=True)
    for h in [
        "SK water withdrawal fell <strong>10.7%</strong> since 2020 — best 5-year result.",
        "SK landfill waste down <strong>29%</strong> since 2022; recovery hit 516k tonnes.",
        "SK certified wood at <strong>58.6%</strong>, highest on record.",
        "WRK renewable energy mix at <strong>60%</strong> of total portfolio.",
        "WRK Scope 3 led by <strong>end-of-life</strong> (Cat 12: 3,172 kt) — a circularity lever.",
        "SK recycled fiber at <strong>76.4%</strong> — consistently high over 5 years.",
    ]:
        st.markdown(f'<div class="highlight-item"><div class="highlight-dot"></div><div>{h}</div></div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3: Forest/Fiber + Energy ──────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌲 Certified Wood Sourcing (SK)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">% of wood from certified forests</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4, 2.2))
    ax.plot(YEARS, sk_certwood, marker="o", color=C["green"], lw=2, ms=6)
    ax.fill_between(YEARS, sk_certwood, 54, alpha=0.08, color=C["green"])
    ax.set_ylim(54, 62); ax.set_xticks(YEARS); ax.set_ylabel("%")
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📦 Recycled Fiber in Production (SK)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">% recycled fiber in global production</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4, 2.2))
    ax.plot(YEARS, sk_recycled, marker="o", color=C["blue"], lw=2, ms=6)
    ax.fill_between(YEARS, sk_recycled, 73, alpha=0.08, color=C["blue"])
    ax.set_ylim(73, 79); ax.set_xticks(YEARS); ax.set_ylabel("%")
    fig_style(fig, ax); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col_f3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ WestRock Energy Mix (2024)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Renewable vs. non-renewable (legacy WRK)</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4, 2.2))
    ax.pie([60,40], labels=["Renewable\n60%","Non-Renewable\n40%"],
           colors=[C["green"],"#ECEFF1"], startangle=90,
           wedgeprops=dict(width=0.5), textprops=dict(fontsize=8, color="#5A6A7A"))
    ax.text(0,0,"60%\nRenewable", ha="center", va="center",
            fontsize=10, fontweight="bold", color=C["navy"])
    fig.patch.set_facecolor("white"); plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Data sources: Smurfit WestRock 2024 Sustainability Report &nbsp;|&nbsp;
  Supporting Data &nbsp;|&nbsp; Supplementary Information &nbsp;|&nbsp; Annual Report &nbsp;|&nbsp; Planet Section<br>
  Prepared for ESG class presentation. Legacy-company data only; consolidated metrics still in development as of 2025.
</div>""", unsafe_allow_html=True)
