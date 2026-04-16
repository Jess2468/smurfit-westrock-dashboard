"""
Smurfit WestRock ESG Performance Dashboard
Deployable Dash application
Data: Legacy Smurfit Kappa (2020-2024) + Legacy WestRock (2024 snapshot)
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── DATA ──────────────────────────────────────────────────────────────────────

YEARS = [2020, 2021, 2022, 2023, 2024]

SK_TREND = pd.DataFrame({
    "Year":                         YEARS,
    "Scope1_ktonnes":               [2545, 2500, 2541, 2415, 2473],
    "Scope2_ktonnes":               [566,  553,  508,  467,  479],
    "Water_Mm3":                    [144.3, 140.1, 141.1, 131.7, 128.9],
    "Waste_Landfill_t":             [442038, 426106, 452757, 370935, 313508],
    "Waste_Recovery_t":             [405801, 475022, 488476, 478944, 516174],
    "Waste_Other_t":                [9022,  14129, 14566, 17336, 23786],
    "Certified_Wood_pct":           [57.3,  56.2,  56.9,  56.8,  58.6],
    "Recycled_Fiber_pct":           [75.4,  75.6,  76.2,  76.5,  76.4],
})
SK_TREND["Scope12_combined"] = SK_TREND["Scope1_ktonnes"] + SK_TREND["Scope2_ktonnes"]
SK_TREND["Total_Waste_t"]    = SK_TREND["Waste_Landfill_t"] + SK_TREND["Waste_Recovery_t"] + SK_TREND["Waste_Other_t"]
SK_TREND["Recovery_Rate_pct"] = (SK_TREND["Waste_Recovery_t"] / SK_TREND["Total_Waste_t"] * 100).round(1)

WRK_2024 = {
    "Scope12_ktonnes":        7974,
    "GHG_intensity":          0.55,
    "Scope3_total":           9452,
    "Scope3_cat1":            2333,
    "Scope3_cat3":            2131,
    "Scope3_cat9":            116,
    "Scope3_cat10":           444,
    "Scope3_cat12":           3172,
    "Recycled_input_pct":     40,
    "Renewable_energy_pct":   60,
    "Water_withdrawal_ML":    470201,
    "Water_intensity":        0.036,
}

SCOPE3_LABELS = [
    "Cat 1 – Purchased goods & services",
    "Cat 3 – Fuel & energy activities",
    "Cat 9 – Downstream transport",
    "Cat 10 – Processing of sold products",
    "Cat 12 – End-of-life treatment",
]
SCOPE3_VALUES = [2333, 2131, 116, 444, 3172]

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────

DARK_NAVY  = "#0d2137"
MID_NAVY   = "#1a3a5c"
TEAL       = "#2a9d8f"
AMBER      = "#e9c46a"
CORAL      = "#e76f51"
LIGHT_GREY = "#f4f6f9"
WHITE      = "#ffffff"
TEXT_DARK  = "#1a1a2e"
TEXT_MID   = "#4a5568"
BORDER     = "#dde3ec"

CHART_FONT = dict(family="Inter, Arial, sans-serif", color=TEXT_DARK)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=CHART_FONT,
    margin=dict(l=10, r=10, t=36, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#e8ecf0", tickfont=dict(size=11)),
    hoverlabel=dict(bgcolor=WHITE, font_size=12, font_family="Inter, Arial"),
)

# ── KPI CARD COMPONENT ────────────────────────────────────────────────────────

def kpi_card(title, value, sub, colour=TEAL, icon="📊"):
    return html.Div([
        html.Div(icon, style={"fontSize": "1.4rem", "marginBottom": "4px"}),
        html.Div(title, style={
            "fontSize": "0.72rem", "fontWeight": "600", "color": TEXT_MID,
            "textTransform": "uppercase", "letterSpacing": "0.05em", "marginBottom": "6px"
        }),
        html.Div(value, style={
            "fontSize": "1.55rem", "fontWeight": "800", "color": colour, "lineHeight": "1.1"
        }),
        html.Div(sub, style={
            "fontSize": "0.68rem", "color": TEXT_MID, "marginTop": "5px", "lineHeight": "1.3"
        }),
    ], style={
        "background": WHITE, "borderRadius": "12px", "padding": "16px 14px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.07)", "flex": "1",
        "minWidth": "155px", "borderTop": f"4px solid {colour}"
    })


# ── CHART BUILDERS ────────────────────────────────────────────────────────────

def fig_scope12():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Scope1_ktonnes"],
        mode="lines+markers", name="Scope 1", line=dict(color=TEAL, width=2.5),
        marker=dict(size=7)))
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Scope2_ktonnes"],
        mode="lines+markers", name="Scope 2", line=dict(color=AMBER, width=2.5),
        marker=dict(size=7)))
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Scope12_combined"],
        mode="lines+markers", name="Scope 1+2", line=dict(color=CORAL, width=2.5, dash="dot"),
        marker=dict(size=7)))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Scope 1 & 2 GHG Trend — Legacy SK (ktonnes CO₂)", font=dict(size=13)),
        yaxis_title="ktonnes CO₂")
    return fig


def fig_water():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Water_Mm3"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(42,157,143,0.12)", line=dict(color=TEAL, width=2.5),
        marker=dict(size=8), name="Water withdrawal"))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Water Withdrawal Trend — Legacy SK (Mm³)", font=dict(size=13)),
        yaxis_title="Mm³")
    return fig


def fig_waste():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=SK_TREND["Year"], y=SK_TREND["Waste_Recovery_t"],
        name="Recovery", marker_color=TEAL, text=SK_TREND["Waste_Recovery_t"].apply(lambda v: f"{v/1000:.0f}k"),
        textposition="inside", insidetextanchor="middle"))
    fig.add_trace(go.Bar(x=SK_TREND["Year"], y=SK_TREND["Waste_Landfill_t"],
        name="Landfill", marker_color=CORAL, text=SK_TREND["Waste_Landfill_t"].apply(lambda v: f"{v/1000:.0f}k"),
        textposition="inside", insidetextanchor="middle"))
    fig.add_trace(go.Bar(x=SK_TREND["Year"], y=SK_TREND["Waste_Other_t"],
        name="Other", marker_color=AMBER))
    fig.update_layout(**PLOTLY_LAYOUT, barmode="stack",
        title=dict(text="Non-Hazardous Waste Pathways — Legacy SK (tonnes)", font=dict(size=13)),
        yaxis_title="tonnes")
    return fig


def fig_scope3():
    colours = [TEAL, "#52b788", AMBER, CORAL, MID_NAVY]
    fig = go.Figure(go.Bar(
        x=SCOPE3_VALUES, y=SCOPE3_LABELS,
        orientation="h",
        marker_color=colours,
        text=[f"{v:,}" for v in SCOPE3_VALUES],
        textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="WestRock 2024 Scope 3 Hotspots (ktonnes CO₂e)", font=dict(size=13)),
        xaxis_title="ktonnes CO₂e",
        yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        margin=dict(l=10, r=60, t=36, b=10))
    return fig


def fig_energy_donut():
    fig = go.Figure(go.Pie(
        labels=["Renewable", "Non-renewable"],
        values=[60, 40],
        hole=0.62,
        marker_colors=[TEAL, CORAL],
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        textfont_size=12,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT, margin=dict(l=10, r=10, t=36, b=10),
        title=dict(text="WRK 2024 Energy Mix", font=dict(size=13)),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
        annotations=[dict(text="<b>60%</b><br>Renewable", x=0.5, y=0.5,
                          font_size=14, showarrow=False)]
    )
    return fig


def fig_circularity():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Recovery_Rate_pct"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in SK_TREND["Recovery_Rate_pct"]],
        textposition="top center",
        line=dict(color=TEAL, width=2.5), marker=dict(size=8), name="Recovery rate"))
    fig.add_trace(go.Scatter(x=SK_TREND["Year"], y=SK_TREND["Recycled_Fiber_pct"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in SK_TREND["Recycled_Fiber_pct"]],
        textposition="bottom center",
        line=dict(color=AMBER, width=2.5, dash="dash"), marker=dict(size=8),
        name="Recycled fiber in production"))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Circularity Metrics — Legacy SK (%)", font=dict(size=13)),
        yaxis_title="%", yaxis=dict(range=[60, 95], showgrid=True, gridcolor="#e8ecf0"))
    return fig


# ── LAYOUT ────────────────────────────────────────────────────────────────────

app = dash.Dash(__name__, title="SW ESG Dashboard")
server = app.server   # expose for gunicorn / cloud deployment

HEADER = html.Div([
    html.Div([
        html.H1("Smurfit WestRock", style={
            "margin": 0, "fontSize": "1.55rem", "fontWeight": "800",
            "color": WHITE, "letterSpacing": "-0.01em"
        }),
        html.Div("ESG Environmental Performance Dashboard · 2020–2024",
                 style={"color": "rgba(255,255,255,0.75)", "fontSize": "0.8rem", "marginTop": "3px"})
    ]),
    html.Div([
        html.Div("⚠️ Data Note: 2024 reporting remains split across two legacy datasets (SK & WRK) "
                 "due to mid-year merger. Do not aggregate across sources.",
                 style={
                     "background": "rgba(233,196,106,0.18)", "border": "1px solid rgba(233,196,106,0.5)",
                     "borderRadius": "8px", "padding": "8px 14px", "fontSize": "0.73rem",
                     "color": AMBER, "maxWidth": "580px", "lineHeight": "1.4"
                 })
    ]),
], style={
    "background": f"linear-gradient(135deg, {DARK_NAVY} 0%, {MID_NAVY} 100%)",
    "padding": "22px 32px", "display": "flex",
    "justifyContent": "space-between", "alignItems": "center",
    "boxShadow": "0 4px 16px rgba(0,0,0,0.18)"
})

KPI_ROW = html.Div([
    kpi_card("SK Scope 1+2 (2024)", "2,952 kt CO₂",
             "Scope 1: 2,473 | Scope 2: 479\n▼ −8.4% vs 2020", TEAL, "🌡️"),
    kpi_card("SK Water Withdrawal", "128.9 Mm³",
             "2024 value | ▼ −10.7% vs 2020\nImproving trend", TEAL, "💧"),
    kpi_card("SK Waste Recovery Rate", "61.8%",
             "516k tonnes recovered in 2024\nLandfill ▼ −29% vs 2020", TEAL, "♻️"),
    kpi_card("SK Recycled Fiber", "76.4%",
             "Share in global production\nStable 2020–2024", AMBER, "🌲"),
    kpi_card("SK Certified Wood", "58.6%",
             "Forest-certified sourcing\nHighest in 5-year period", AMBER, "🏔️"),
    kpi_card("WRK Scope 1+2 (2024)", "7,974 kt CO₂e",
             "Intensity: 0.55 tCO₂e / ton\nLegacy WestRock only", CORAL, "🏭"),
    kpi_card("WRK Renewable Energy", "60%",
             "Of total energy mix\nNon-renewable: 40%", CORAL, "⚡"),
], style={
    "display": "flex", "flexWrap": "wrap", "gap": "12px",
    "padding": "20px 32px 8px", "background": LIGHT_GREY
})

CHART_SECTION = html.Div([
    # Row 1 – GHG & Water
    html.Div([
        html.Div(dcc.Graph(figure=fig_scope12(), config={"displayModeBar": False}),
                 style={"flex": "1", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div(dcc.Graph(figure=fig_water(), config={"displayModeBar": False}),
                 style={"flex": "1", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

    # Row 2 – Waste & Scope 3
    html.Div([
        html.Div(dcc.Graph(figure=fig_waste(), config={"displayModeBar": False}),
                 style={"flex": "1.2", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div(dcc.Graph(figure=fig_scope3(), config={"displayModeBar": False}),
                 style={"flex": "1", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

    # Row 3 – Circularity & Energy
    html.Div([
        html.Div(dcc.Graph(figure=fig_circularity(), config={"displayModeBar": False}),
                 style={"flex": "1.4", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div(dcc.Graph(figure=fig_energy_donut(), config={"displayModeBar": False}),
                 style={"flex": "0.8", "background": WHITE, "borderRadius": "12px",
                        "padding": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        # Key insights card
        html.Div([
            html.Div("📌 Key Insights", style={
                "fontWeight": "700", "fontSize": "0.85rem", "color": TEXT_DARK,
                "marginBottom": "10px", "textTransform": "uppercase", "letterSpacing": "0.05em"
            }),
            *[html.Div([
                html.Span("●  ", style={"color": TEAL, "fontWeight": "700"}),
                html.Span(txt, style={"fontSize": "0.78rem", "color": TEXT_MID, "lineHeight": "1.45"})
              ], style={"marginBottom": "9px"}) for txt in [
                "SK Scope 1+2 fell 8.4% (2020→2024), led by Scope 2 reductions.",
                "Water withdrawal improved 10.7%; strongest gains 2022→2024.",
                "SK landfill waste down 29% while recovery tonnes rose 27%.",
                "WRK Scope 3 Cat 12 (end-of-life) is the single largest hotspot at 3,172 kt.",
                "60% renewable energy (WRK) — on track for decarbonisation.",
                "Certified wood share hit 5-year high of 58.6% in 2024.",
                "Disclosure gap: combined consolidated targets not yet published.",
            ]]
        ], style={
            "flex": "0.9", "background": WHITE, "borderRadius": "12px",
            "padding": "18px 16px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
        }),
    ], style={"display": "flex", "gap": "16px"}),
], style={"padding": "12px 32px 20px", "background": LIGHT_GREY})

FOOTER = html.Div(
    "Sources: Smurfit WestRock 2024 Sustainability Report · Supporting Data · Supplementary Information · "
    "Annual Report · Planet Section  |  Dashboard prepared for IIT Chicago ESG Analytics class · "
    "Jeslyn Jose & Emilio  |  Data reflects legacy-company boundaries; combined 2024 disclosures pending.",
    style={
        "background": DARK_NAVY, "color": "rgba(255,255,255,0.5)", "padding": "12px 32px",
        "fontSize": "0.67rem", "textAlign": "center", "lineHeight": "1.5"
    }
)

app.layout = html.Div(
    [HEADER, KPI_ROW, CHART_SECTION, FOOTER],
    style={"fontFamily": "Inter, Arial, sans-serif", "background": LIGHT_GREY, "minHeight": "100vh"}
)

# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
