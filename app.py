import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# ─── โหลดข้อมูล ───────────────────────────────────────────────────────────────
# ตรวจสอบ path ไฟล์ให้ตรงกับที่คุณเซฟไว้
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
        "color": COLORS["text"],
        "minHeight": "100vh",
        "fontFamily": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
        "padding": "30px",
    },
    children=[
        # Header
        html.Div(
            [
                html.H1(
                    "Hotel Revenue Forecasting Dashboard",
                    style={"margin": "0 0 10px 0", "color": COLORS["text"]},
                ),
                html.P(
                    "ระบบพยากรณ์รายได้สถานประกอบการที่พักแรม โดยใช้ Machine Learning (AutoGluon)",
                    style={"color": COLORS["muted"], "margin": "0 0 20px 0"},
                ),
            ],
            style={
                "borderBottom": f"1px solid {COLORS['border']}",
                "paddingBottom": "20px",
                "marginBottom": "30px",
            },
        ),
        # Control Panel
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "30px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    [
                        html.Label(
                            "เลือกภูมิภาค (Region):",
                            style={
                                "display": "block",
                                "marginBottom": "8px",
                                "color": COLORS["muted"],
                            },
                        ),
                        dcc.Dropdown(
                            id="region-dropdown",
                            options=[
                                {"label": REGION_TH.get(r, r), "value": r}
                                for r in REGIONS
                            ],
                            value="Bangkok",
                            clearable=False,
                            style={"color": "#000"},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "250px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "เลือกขนาดห้องพัก (Size):",
                            style={
                                "display": "block",
                                "marginBottom": "8px",
                                "color": COLORS["muted"],
                            },
                        ),
                        dcc.Dropdown(
                            id="size-dropdown",
                            options=[
                                {"label": SIZE_LABEL.get(s, s), "value": s}
                                for s in SIZES
                            ],
                            value=1,
                            clearable=False,
                            style={"color": "#000"},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "250px"},
                ),
            ],
        ),
        html.Div(
            style={
                "backgroundColor": COLORS["card"],
                "padding": "25px",
                "borderRadius": "10px",
                "border": f"1px solid {COLORS['border']}",
                "marginBottom": "30px",
            },
            children=[
                html.H3(
                    "🌟 โมดูลจำลองสถานการณ์ (What-If Scenario Simulator)",
                    style={"marginTop": "0", "color": COLORS["forecast"]},
                ),
                html.P(
                    "ทดลองปรับเปลี่ยน 'ปริมาณนักท่องเที่ยวในอนาคต' เพื่อดูผลกระทบต่อแนวโน้มรายได้ (Exogenous Variable Analysis)",
                    style={"color": COLORS["muted"], "fontSize": "14px"},
                ),
                html.Div(
                    [
                        dcc.Slider(
                            id="tourist-slider",
                            min=-50,
                            max=50,
                            step=None,
                            value=0,
                            marks={
                                i: {
                                    "label": f"{i}%",
                                    "style": {"color": COLORS["text"]},
                                }
                                for i in range(-50, 51, 5)
                            },
                        )
                    ],
                    style={"padding": "10px 0"},
                ),
            ],
        ),
        # Graph Area
        html.Div(
            style={
                "backgroundColor": COLORS["card"],
                "padding": "20px",
                "borderRadius": "10px",
                "border": f"1px solid {COLORS['border']}",
            },
            children=[dcc.Graph(id="main-graph", config={"displayModeBar": False})],
        ),
    ],
)


# ─── Callbacks ────────────────────────────────────────────────────────────────
@app.callback(
    Output("main-graph", "figure"),
    [
        Input("region-dropdown", "value"),
        Input("size-dropdown", "value"),
        Input("tourist-slider", "value"),
    ],  # รับค่าจาก Slider
)
def update_dashboard(region, size, tourist_adj):
    # กรองข้อมูล
    mask = (df["region"] == region) & (df["size_rank"] == size)
    dff = df[mask].sort_values("year_th").copy()

    actual_df = dff[dff["type"] == "actual"].copy()
    forecast_df = dff[dff["type"] == "forecast"].copy()

    # 🌟 การทำงานของโมดูล: คำนวณรายได้ใหม่ตามการปรับเปลี่ยนของนักท่องเที่ยว
    # สมมติฐาน: ถ้านักท่องเที่ยวเปลี่ยน X% รายได้จะเปลี่ยนตามสัดส่วนนั้น
    adjustment_factor = 1 + (tourist_adj / 100.0)

    if not forecast_df.empty:
        forecast_df["value"] = forecast_df["value"] * adjustment_factor
        forecast_df["lower"] = forecast_df["lower"] * adjustment_factor
        forecast_df["upper"] = forecast_df["upper"] * adjustment_factor
        # อัปเดตตัวเลขนักท่องเที่ยวจำลองเพื่อแสดงผลใน Hover
        forecast_df["tourists_mn"] = forecast_df["tourists_mn"] * adjustment_factor

    fig = go.Figure()

    # 1. Plot Actual
    fig.add_trace(
        go.Scatter(
            x=actual_df["year_th"],
            y=actual_df["value"],
            mode="lines+markers",
            name="ข้อมูลจริง (Actual)",
            line=dict(color=COLORS["actual"], width=3),
            marker=dict(size=8),
            hovertemplate="ปี พ.ศ. %{x}<br>รายได้: ฿%{y:,.0f}<br>นักท่องเที่ยว: %{customdata:,.0f} คน<extra></extra>",
            customdata=actual_df["tourists_mn"],
        )
    )

    # เส้นเชื่อมระหว่าง Actual และ Forecast
    if not actual_df.empty and not forecast_df.empty:
        last_actual = actual_df.iloc[-1:]
        first_forecast = forecast_df.iloc[:1]
        connector = pd.concat([last_actual, first_forecast])
        fig.add_trace(
            go.Scatter(
                x=connector["year_th"],
                y=connector["value"],
                mode="lines",
                showlegend=False,
                line=dict(color=COLORS["forecast"], width=3, dash="dash"),
            )
        )

    # 2. Plot Forecast
    if not forecast_df.empty:
        fig.add_trace(
            go.Scatter(
                x=forecast_df["year_th"],
                y=forecast_df["value"],
                mode="lines+markers",
                name=f"ผลพยากรณ์ (ปรับนักท่องเที่ยว {tourist_adj:+}%)",
                line=dict(color=COLORS["forecast"], width=3, dash="dash"),
                marker=dict(size=8),
                hovertemplate="ปี พ.ศ. %{x}<br>รายได้พยากรณ์: ฿%{y:,.0f}<br>นักท่องเที่ยว (จำลอง): %{customdata:,.0f} คน<extra></extra>",
                customdata=forecast_df["tourists_mn"],
            )
        )

        # Plot Confidence Interval (Lower-Upper Bound)
        fig.add_trace(
            go.Scatter(
                x=list(forecast_df["year_th"]) + list(forecast_df["year_th"])[::-1],
                y=list(forecast_df["upper"]) + list(forecast_df["lower"])[::-1],
                fill="toself",
                fillcolor=COLORS["band"],
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                name="ช่วงความน่าจะเป็น (80% CI)",
            )
        )

    fig.update_layout(
        title=f"แนวโน้มรายได้โรงแรม: {REGION_TH.get(region, region)} - {SIZE_LABEL.get(size, size)}",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=COLORS["bg"],  # สีพื้นหลังกล่องเป็นสีดำเข้ม
            font_color=COLORS["text"],  # สีตัวหนังสือเป็นสีขาว
            bordercolor=COLORS["border"],  # สีเส้นขอบ
            font_size=14,  # ปรับขนาดฟอนต์ให้อ่านง่ายขึ้น
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(title="ปี พ.ศ.", gridcolor=COLORS["border"]),
        yaxis=dict(title="รายได้ (บาท)", gridcolor=COLORS["border"]),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
