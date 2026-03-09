import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# ─── โหลดข้อมูล ───────────────────────────────────────────────────────────────
df = pd.read_csv("data/predict/predictions.csv")

SIZE_LABEL = {
    1: "เล็ก (น้อยกว่า 60 ห้อง)",
    2: "กลาง (60 ถึง 149 ห้อง)",
    3: "ใหญ่ (150 ห้องขึ้นไป)",
}
REGION_TH = {
    "Bangkok": "กรุงเทพมหานคร",
    "Central": "ภาคกลาง",
    "Northern": "ภาคเหนือ",
    "Northeastern": "ภาคตะวันออกเฉียงเหนือ",
    "Southern": "ภาคใต้",
}
REGIONS = sorted(df["region"].unique())
SIZES = sorted(df["size_rank"].unique())

COLORS = {
    "actual": "#4FC3F7",
    "forecast": "#FFB74D",
    "band": "rgba(255,183,77,0.15)",
    "bg": "#0D1117",
    "card": "#202B3A",
    "border": "#30363D",
    "text": "#FFFFFF",
    "muted": "#8B949E",
}

# ─── App ──────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="Hotel Revenue Forecast")

app.layout = html.Div(
    style={
        "backgroundColor": COLORS["bg"],
        "minHeight": "100vh",
        "fontFamily": "'IBM Plex Sans Thai', 'Sarabun', sans-serif",
        "color": COLORS["text"],
        "padding": "32px",
    },
    children=[
        # Header
        html.Div(
            style={
                "marginBottom": "32px",
                "borderBottom": f"1px solid {COLORS['border']}",
                "paddingBottom": "24px",
            },
            children=[
                html.H1(
                    "🏨 Hotel Revenue Forecast",
                    style={
                        "fontSize": "28px",
                        "fontWeight": "700",
                        "margin": "0 0 6px 0",
                        "letterSpacing": "-0.5px",
                    },
                ),
                html.P(
                    "รายได้โรงแรมจำแนกตามภูมิภาคและขนาด · ข้อมูล สสช.",
                    style={"color": COLORS["muted"], "margin": 0, "fontSize": "16px"},
                ),
            ],
        ),
        # Controls
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "16px",
                "marginBottom": "24px",
            },
            children=[
                html.Div(
                    [
                        html.Label(
                            "ภูมิภาค",
                            style={
                                "fontSize": "18px",
                                "color": COLORS["text"],
                                "marginBottom": "8px",
                                "display": "block",
                                "letterSpacing": "1px",
                            },
                        ),
                        dcc.Checklist(
                            id="region-filter",
                            options=[
                                {"label": f"  {REGION_TH.get(r, r)}", "value": r}
                                for r in REGIONS
                            ],
                            value=REGIONS,
                            inline=True,
                            style={"fontSize": "16px"},
                            inputStyle={
                                "marginRight": "4px",
                                "accentColor": COLORS["forecast"],
                            },
                            labelStyle={
                                "marginRight": "16px",
                                "color": COLORS["muted"],
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": COLORS["card"],
                        "padding": "16px",
                        "borderRadius": "8px",
                        "border": f"1px solid {COLORS['border']}",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "ขนาดโรงแรม",
                            style={
                                "fontSize": "18px",
                                "color": COLORS["text"],
                                "marginBottom": "8px",
                                "display": "block",
                                "letterSpacing": "1px",
                            },
                        ),
                        dcc.Checklist(
                            id="size-filter",
                            options=[
                                {"label": f"  {SIZE_LABEL[s]}", "value": s}
                                for s in SIZES
                            ],
                            value=SIZES,
                            inline=True,
                            style={"fontSize": "16px"},
                            inputStyle={
                                "marginRight": "4px",
                                "accentColor": COLORS["actual"],
                            },
                            labelStyle={
                                "marginRight": "16px",
                                "color": COLORS["muted"],
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": COLORS["card"],
                        "padding": "16px",
                        "borderRadius": "8px",
                        "border": f"1px solid {COLORS['border']}",
                    },
                ),
            ],
        ),
        # Main chart
        html.Div(
            style={
                "backgroundColor": COLORS["card"],
                "borderRadius": "12px",
                "border": f"1px solid {COLORS['border']}",
                "padding": "24px",
                "marginBottom": "24px",
            },
            children=[
                html.Div(
                    id="chart-title",
                    style={
                        "fontSize": "15px",
                        "fontWeight": "600",
                        "marginBottom": "16px",
                        "color": COLORS["text"],
                    },
                ),
                dcc.Graph(
                    id="main-chart",
                    style={"height": "420px"},
                    config={"displayModeBar": False},
                ),
            ],
        ),
        # Summary cards
        html.Div(
            id="summary-cards",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(5, 1fr)",
                "gap": "12px",
            },
        ),
        # Footer
        html.P(
            "Forecast ใช้ Chronos2 · ช่วงสีคือ 80% confidence interval (quantile 0.1–0.9)",
            style={
                "textAlign": "center",
                "color": COLORS["muted"],
                "fontSize": "12px",
                "marginTop": "32px",
            },
        ),
    ],
)


# ─── Callback ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("main-chart", "figure"),
    Output("chart-title", "children"),
    Output("summary-cards", "children"),
    Input("region-filter", "value"),
    Input("size-filter", "value"),
)
def update(selected_regions, selected_sizes):
    if not selected_regions or not selected_sizes:
        empty = go.Figure()
        empty.update_layout(paper_bgcolor=COLORS["card"], plot_bgcolor=COLORS["card"])
        return empty, "ไม่มีข้อมูล", []

    filtered = df[
        df["region"].isin(selected_regions) & df["size_rank"].isin(selected_sizes)
    ]
    actual_df = filtered[filtered["type"] == "actual"]
    forecast_df = filtered[filtered["type"] == "forecast"]

    # รวม aggregate ตาม year
    agg_actual = actual_df.groupby("year_th")["value"].sum().reset_index()
    agg_forecast = (
        forecast_df.groupby("year_th")
        .agg(value=("value", "sum"), lower=("lower", "sum"), upper=("upper", "sum"))
        .reset_index()
    )

    fig = go.Figure()

    # Confidence band
    if not agg_forecast.empty:
        fig.add_trace(
            go.Scatter(
                x=pd.concat([agg_forecast["year_th"], agg_forecast["year_th"][::-1]]),
                y=pd.concat([agg_forecast["upper"], agg_forecast["lower"][::-1]]),
                fill="toself",
                fillcolor=COLORS["band"],
                line=dict(color="rgba(0,0,0,0)"),
                name="80% Confidence",
                hoverinfo="skip",
            )
        )

    # Actual line
    fig.add_trace(
        go.Scatter(
            x=agg_actual["year_th"],
            y=agg_actual["value"],
            mode="lines+markers",
            line=dict(color=COLORS["actual"], width=2.5),
            marker=dict(size=7, color=COLORS["actual"]),
            name="ข้อมูลจริง",
        )
    )

    # เส้นเชื่อม actual → forecast
    if not agg_actual.empty and not agg_forecast.empty:
        fig.add_trace(
            go.Scatter(
                x=[agg_actual["year_th"].iloc[-1], agg_forecast["year_th"].iloc[0]],
                y=[agg_actual["value"].iloc[-1], agg_forecast["value"].iloc[0]],
                mode="lines",
                line=dict(color=COLORS["forecast"], width=2, dash="dot"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Forecast line
    fig.add_trace(
        go.Scatter(
            x=agg_forecast["year_th"],
            y=agg_forecast["value"],
            mode="lines+markers",
            line=dict(color=COLORS["forecast"], width=2.5, dash="dash"),
            marker=dict(size=8, color=COLORS["forecast"], symbol="diamond"),
            name="Forecast",
        )
    )

    # เส้นแบ่ง actual/forecast
    fig.add_vline(
        x=2558.5,
        line_dash="dot",
        line_color=COLORS["muted"],
        line_width=1,
        annotation_text="Forecast →",
        annotation_font_color=COLORS["muted"],
        annotation_font_size=11,
    )

    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["bg"],
        font=dict(
            color=COLORS["text"], family="IBM Plex Sans Thai, Sarabun, sans-serif"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=COLORS["border"],
            borderwidth=1,
            font=dict(size=12),
        ),
        xaxis=dict(
            gridcolor=COLORS["border"],
            title="ปี พ.ศ.",
            tickvals=sorted(filtered["year_th"].unique()),
        ),
        yaxis=dict(gridcolor=COLORS["border"], title="รายได้ (บาท)", tickformat=",.0f"),
        margin=dict(l=16, r=16, t=8, b=8),
        hovermode="x unified",
    )

    n_region = len(selected_regions)
    n_size = len(selected_sizes)
    title = f"รายได้รวม · {n_region} ภูมิภาค · {n_size} ขนาด"

    # Summary cards (forecast per region)
    cards = []
    for reg in selected_regions:
        reg_f = forecast_df[forecast_df["region"] == reg]
        if reg_f.empty:
            continue
        total = reg_f.groupby("year_th")["value"].sum()
        latest_year = total.index.max()
        latest_val = total[latest_year]
        cards.append(
            html.Div(
                style={
                    "backgroundColor": COLORS["card"],
                    "borderRadius": "8px",
                    "border": f"1px solid {COLORS['border']}",
                    "padding": "16px",
                },
                children=[
                    html.P(
                        REGION_TH.get(reg, reg),
                        style={
                            "fontSize": "11px",
                            "color": COLORS["muted"],
                            "margin": "0 0 6px 0",
                            "letterSpacing": "0.5px",
                        },
                    ),
                    html.P(
                        f"ปี {latest_year}",
                        style={
                            "fontSize": "12px",
                            "color": COLORS["muted"],
                            "margin": "0 0 4px 0",
                        },
                    ),
                    html.P(
                        f"฿{latest_val/1e9:.1f}B",
                        style={
                            "fontSize": "22px",
                            "fontWeight": "700",
                            "color": COLORS["forecast"],
                            "margin": 0,
                        },
                    ),
                ],
            )
        )

    return fig, title, cards


if __name__ == "__main__":
    app.run(debug=True)
