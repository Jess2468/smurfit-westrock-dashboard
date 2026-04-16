import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smurfit Westrock ESG Performance Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');

    /* Global */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1400px; }
    html, body, [class*="css"] { font-family: 'Source Sans Pro', sans-serif; }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #1B2A3D 0%, #263B50 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .header-title { color: #FFFFFF; font-size: 1.85rem; font-weight: 700; margin: 0; line-height: 1.2; }
    .header-subtitle { color: #A8B8C8; font-size: 0.85rem; margin-top: 4px; }
    .header-badge {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.25);
        color: #7FDBCA;
        padding: 8px 18px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* KPI cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.1rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .kpi-label-tag {
        display: inline-block;
        background: #1B6B5A;
        color: #FFFFFF;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .kpi-name { color: #1E293B; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px; }
    .kpi-value { color: #0F172A; font-size: 1.65rem; font-weight: 700; line-height: 1.15; }
    .kpi-detail { color: #64748B; font-size: 0.7rem; margin-top: 3px; }

    /* Section cards */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 0.5rem;
    }
    .section-title { color: #0F172A; font-size: 1.1rem; font-weight: 700; margin-bottom: 2px; }
    .section-subtitle { color: #64748B; font-size: 0.78rem; margin-bottom: 0.5rem; }

    /* Strategic highlights */
    .highlight-item {
        padding: 8px 0;
        border-bottom: 1px solid #F1F5F9;
        color: #1E293B;
        font-size: 0.82rem;
        line-height: 1.45;
    }
    .highlight-item:last-child { border-bottom: none; }
    .highlight-bullet { color: #1B6B5A; font-weight: 700; margin-right: 6px; }

    /* Footer */
    .footer-text { color: #64748B; font-size: 0.72rem; text-align: center; margin-top: 1.5rem; padding: 1rem; border-top: 1px solid #E2E8F0; }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────
sk_trend = pd.DataFrame({
    "Year": [2020, 2021, 2022, 2023, 2024],
    "Scope 1 (ktonnes CO2)": [2545, 2500, 2541, 2415, 2473],
    "Scope 2 (ktonnes CO2)": [566, 553, 508, 467, 479],
    "Water Withdrawal (Mm3)": [144.3, 140.1, 141.1, 131.7, 128.9],
    "Landfill Waste (tonnes)": [442038, 426106, 452757, 370935, 313508],
    "Recovered Waste (tonnes)": [405801, 475022, 488476, 478944, 516174],
    "Other Waste (tonnes)": [9022, 14129, 14566, 17336, 23786],
    "Certified Wood (pct)": [57.3, 56.2, 56.9, 56.8, 58.6],
    "Recycled Fiber (pct)": [75.4, 75.6, 76.2, 76.5, 76.4],
})
sk_trend["Scope 1+2"] = sk_trend["Scope 1 (ktonnes CO2)"] + sk_trend["Scope 2 (ktonnes CO2)"]
sk_trend["Total Waste"] = sk_trend["Landfill Waste (tonnes)"] + sk_trend["Recovered Waste (tonnes)"] + sk_trend["Other Waste (tonnes)"]
sk_trend["Recovery Rate (pct)"] = (sk_trend["Recovered Waste (tonnes)"] / sk_trend["Total Waste"] * 100).round(1)

wrk_2024 = {
    "Scope 1+2 (ktonnes CO2e)": 7974,
    "GHG Intensity": 0.55,
    "Scope 3 Total": 9452,
    "Recycled Input": 40,
    "Renewable Energy": 60,
    "Water Withdrawal (ML)": 470201,
    "Water Intensity": 0.036,
}

wrk_scope3 = pd.DataFrame({
    "Category": [
        "Cat 1 - Purchased goods",
        "Cat 3 - Fuel and energy",
        "Cat 9 - Downstream transport",
        "Cat 10 - Processing sold products",
        "Cat 12 - End-of-life treatment",
    ],
    "Emissions": [2333, 2131, 116, 444, 3172],
})

materiality = pd.DataFrame({
    "Topic": [
        "Climate Change", "Circular Economy", "Sustainable Forestry",
        "Water Management", "Energy Efficiency", "Pollution",
        "Biodiversity", "Supply Chain Sustainability",
    ],
    "Business Impact": [10.0, 9.5, 9.0, 8.2, 8.8, 7.5, 7.0, 8.5],
    "Stakeholder Importance": [10.2, 9.4, 9.0, 8.2, 8.0, 7.8, 7.2, 8.8],
})

# ── Chart style defaults ─────────────────────────────────────────────────────
CHART_FONT = dict(family="Source Sans Pro, sans-serif", size=14, color="#0F172A")
AXIS_STYLE = dict(
    gridcolor="#E2E8F0",
    linecolor="#94A3B8",
    tickfont=dict(size=13, color="#334155"),
    title_font=dict(size=14, color="#0F172A", family="Source Sans Pro"),
)
CHART_MARGIN = dict(l=60, r=30, t=40, b=50)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div>
        <div class="header-title">Smurfit Westrock ESG Performance Dashboard</div>
        <div class="header-subtitle">Environmental metrics, material issues, and progress toward targets - Dashboard based on 2024 sustainability disclosures</div>
    </div>
    <div class="header-badge">2024 Focus - Legacy Data - Status: Disclosure Transition</div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ──────────────────────────────────────────────────────────────────
def kpi_card(name, value, detail):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label-tag">KPI</div>
        <div class="kpi-name">{name}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-detail">{detail}</div>
    </div>"""

latest = sk_trend[sk_trend["Year"] == 2024].iloc[0]
prev = sk_trend[sk_trend["Year"] == 2023].iloc[0]
scope12_yoy = ((latest["Scope 1+2"] - prev["Scope 1+2"]) / prev["Scope 1+2"] * 100)
water_yoy = ((latest["Water Withdrawal (Mm3)"] - prev["Water Withdrawal (Mm3)"]) / prev["Water Withdrawal (Mm3)"] * 100)

cols = st.columns(6)
kpis = [
    ("SK Scope 1+2 Combined", f"{latest['Scope 1+2']:,.0f} kt CO2",
     f"YoY: {scope12_yoy:+.1f}% - Legacy Smurfit Kappa"),
    ("WRK Scope 1+2 (MBM)", f"{wrk_2024['Scope 1+2 (ktonnes CO2e)']:,.0f} kt CO2e",
     f"Intensity: {wrk_2024['GHG Intensity']} tCO2e/ton - Legacy WestRock"),
    ("WRK Renewable Energy", f"{wrk_2024['Renewable Energy']}%",
     f"Non-renewable: {100 - wrk_2024['Renewable Energy']}% - Legacy WestRock"),
    ("SK Recycled Fiber", f"{latest['Recycled Fiber (pct)']}%",
     f"Certified wood: {latest['Certified Wood (pct)']}% - Legacy SK"),
    ("SK Water Withdrawal", f"{latest['Water Withdrawal (Mm3)']} Mm3",
     f"YoY: {water_yoy:+.1f}% - Legacy Smurfit Kappa"),
    ("SK Waste Recovery Rate", f"{latest['Recovery Rate (pct)']:.1f}%",
     f"Recovery: {latest['Recovered Waste (tonnes)']:,.0f}t - Legacy SK"),
]
for i, (name, value, detail) in enumerate(kpis):
    with cols[i]:
        st.markdown(kpi_card(name, value, detail), unsafe_allow_html=True)

st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)

# ── ROW 2: Climate + Materiality ─────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""<div class="section-card">
        <div class="section-title">Climate Progress - Smurfit Kappa Legacy</div>
        <div class="section-subtitle">Scope 1, Scope 2, and combined emissions trend (2020-2024) in ktonnes CO2</div>
    </div>""", unsafe_allow_html=True)

    fig_climate = go.Figure()
    fig_climate.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Scope 1 (ktonnes CO2)"],
        name="Scope 1", mode="lines+markers",
        line=dict(color="#2563EB", width=3.5), marker=dict(size=10),
    ))
    fig_climate.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Scope 2 (ktonnes CO2)"],
        name="Scope 2", mode="lines+markers",
        line=dict(color="#F59E0B", width=3.5), marker=dict(size=10),
    ))
    fig_climate.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Scope 1+2"],
        name="Scope 1+2", mode="lines+markers",
        line=dict(color="#DC2626", width=3.5, dash="dot"), marker=dict(size=10),
    ))
    fig_climate.update_layout(
        height=380, margin=CHART_MARGIN,
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center",
                    font=dict(size=14, color="#0F172A")),
        xaxis=dict(**AXIS_STYLE, title="Year", dtick=1),
        yaxis=dict(**AXIS_STYLE, title="ktonnes CO2"),
        font=CHART_FONT,
    )
    st.plotly_chart(fig_climate, use_container_width=True)

with col_right:
    st.markdown("""<div class="section-card">
        <div class="section-title">Materiality Matrix</div>
        <div class="section-subtitle">Topics with the highest business impact and stakeholder importance</div>
    </div>""", unsafe_allow_html=True)

    fig_mat = go.Figure()
    fig_mat.add_trace(go.Scatter(
        x=materiality["Business Impact"],
        y=materiality["Stakeholder Importance"],
        mode="markers+text",
        text=materiality["Topic"],
        textposition="top center",
        textfont=dict(size=12, color="#0F172A", family="Source Sans Pro"),
        marker=dict(
            size=24, color="#2B7A6F", opacity=0.85,
            line=dict(color="#1B5E50", width=2),
        ),
    ))
    fig_mat.update_layout(
        height=380, margin=CHART_MARGIN,
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(**AXIS_STYLE, title="Business Impact", range=[6.5, 10.8]),
        yaxis=dict(**AXIS_STYLE, title="Stakeholder Importance", range=[6.5, 10.8]),
        font=CHART_FONT,
        showlegend=False,
    )
    st.plotly_chart(fig_mat, use_container_width=True)

# ── ROW 3: Scope 3 + Circularity + Highlights ───────────────────────────────
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""<div class="section-card">
        <div class="section-title">WestRock Scope 3 Hotspots (2024)</div>
        <div class="section-subtitle">Largest value-chain emission categories in ktonnes CO2e</div>
    </div>""", unsafe_allow_html=True)

    fig_s3 = go.Figure()
    fig_s3.add_trace(go.Bar(
        y=wrk_scope3["Category"],
        x=wrk_scope3["Emissions"],
        orientation="h",
        marker_color=["#1D4ED8", "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD"],
        text=wrk_scope3["Emissions"].apply(lambda v: f"{v:,.0f}"),
        textposition="outside",
        textfont=dict(size=13, color="#0F172A"),
    ))
    fig_s3.update_layout(
        height=380, margin=dict(l=10, r=70, t=30, b=40),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(**AXIS_STYLE, title="ktonnes CO2e"),
        yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#334155")),
        font=CHART_FONT,
        showlegend=False,
    )
    st.plotly_chart(fig_s3, use_container_width=True)

with col_b:
    st.markdown("""<div class="section-card">
        <div class="section-title">Circularity and Waste - SK Legacy</div>
        <div class="section-subtitle">Waste pathways: landfill, recovery, and other (2020-2024)</div>
    </div>""", unsafe_allow_html=True)

    fig_waste = go.Figure()
    fig_waste.add_trace(go.Bar(
        x=sk_trend["Year"], y=sk_trend["Landfill Waste (tonnes)"] / 1000,
        name="Landfill", marker_color="#DC2626",
    ))
    fig_waste.add_trace(go.Bar(
        x=sk_trend["Year"], y=sk_trend["Recovered Waste (tonnes)"] / 1000,
        name="Recovery", marker_color="#2B7A6F",
    ))
    fig_waste.add_trace(go.Bar(
        x=sk_trend["Year"], y=sk_trend["Other Waste (tonnes)"] / 1000,
        name="Other", marker_color="#F59E0B",
    ))
    fig_waste.update_layout(
        barmode="stack", height=380,
        margin=CHART_MARGIN,
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center",
                    font=dict(size=13, color="#0F172A")),
        xaxis=dict(**AXIS_STYLE, title="Year", dtick=1),
        yaxis=dict(**AXIS_STYLE, title="Thousand tonnes"),
        font=CHART_FONT,
    )
    st.plotly_chart(fig_waste, use_container_width=True)

with col_c:
    st.markdown("""<div class="section-card">
        <div class="section-title">Strategic Highlights</div>
        <div class="section-subtitle">Key signals from the 2024 legacy datasets</div>
    """, unsafe_allow_html=True)

    highlights = [
        f"SK Scope 1+2 emissions were <b>{latest['Scope 1+2']:,.0f} ktonnes</b> in 2024, "
        f"a {scope12_yoy:+.1f}% change YoY. Scope 2 fell 15% since 2020.",
        f"WestRock Scope 3 totalled <b>9,452 ktonnes CO2e</b>; end-of-life treatment "
        f"is the largest category at 3,172 kt.",
        f"SK water withdrawal dropped to <b>{latest['Water Withdrawal (Mm3)']} Mm3</b>, "
        f"down 10.7% vs 2020, showing consistent improvement.",
        f"Waste recovery reached <b>{latest['Recovered Waste (tonnes)']:,.0f} tonnes</b> "
        f"({latest['Recovery Rate (pct)']:.1f}% recovery rate), up from 47.4% in 2020.",
        f"Certified wood share rose to <b>{latest['Certified Wood (pct)']}%</b> in 2024, "
        f"the highest since 2020, supporting forestry materiality.",
        f"WestRock energy mix is <b>60% renewable</b>; recycled input materials at 40%.",
        "2024 data is still primarily <b>legacy-company based</b> - consolidated "
        "targets are being developed in 2025.",
    ]
    for h in highlights:
        st.markdown(
            f'<div class="highlight-item"><span class="highlight-bullet">*</span> {h}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ── ROW 4: Water + Forest ────────────────────────────────────────────────────
col_w, col_f = st.columns(2)

with col_w:
    st.markdown("""<div class="section-card">
        <div class="section-title">Water Withdrawal Trend - SK Legacy</div>
        <div class="section-subtitle">Total water withdrawal in million m3 (2020-2024)</div>
    </div>""", unsafe_allow_html=True)

    fig_water = go.Figure()
    fig_water.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Water Withdrawal (Mm3)"],
        mode="lines+markers+text",
        text=sk_trend["Water Withdrawal (Mm3)"].apply(lambda v: f"{v:.1f}"),
        textposition="top center", textfont=dict(size=13, color="#0F172A"),
        line=dict(color="#2563EB", width=3.5), marker=dict(size=11, color="#2563EB"),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.1)",
    ))
    fig_water.update_layout(
        height=340, margin=CHART_MARGIN,
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        xaxis=dict(**AXIS_STYLE, title="Year", dtick=1),
        yaxis=dict(**AXIS_STYLE, title="Mm3", range=[120, 155]),
        font=CHART_FONT,
        showlegend=False,
    )
    st.plotly_chart(fig_water, use_container_width=True)

with col_f:
    st.markdown("""<div class="section-card">
        <div class="section-title">Forest and Fiber Metrics - SK Legacy</div>
        <div class="section-subtitle">Certified wood sourcing and recycled fiber share (2020-2024)</div>
    </div>""", unsafe_allow_html=True)

    fig_fiber = go.Figure()
    fig_fiber.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Certified Wood (pct)"],
        name="Certified Wood (%)", mode="lines+markers",
        line=dict(color="#2B7A6F", width=3.5), marker=dict(size=10),
    ))
    fig_fiber.add_trace(go.Scatter(
        x=sk_trend["Year"], y=sk_trend["Recycled Fiber (pct)"],
        name="Recycled Fiber (%)", mode="lines+markers",
        line=dict(color="#F59E0B", width=3.5), marker=dict(size=10),
    ))
    fig_fiber.update_layout(
        height=340, margin=CHART_MARGIN,
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center",
                    font=dict(size=14, color="#0F172A")),
        xaxis=dict(**AXIS_STYLE, title="Year", dtick=1),
        yaxis=dict(**AXIS_STYLE, title="%", range=[50, 80]),
        font=CHART_FONT,
    )
    st.plotly_chart(fig_fiber, use_container_width=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-text">
    Prepared from Smurfit Westrock 2024 sustainability disclosures (Supporting Data and Supplementary Information).
    Legacy-company data - 2024 reporting is still primarily legacy-company based because the combination closed mid-year.
    Consolidated targets and KPIs are still being developed in 2025. | ESC Analytics and Management - Lab 4 Dashboard
</div>
""", unsafe_allow_html=True)
