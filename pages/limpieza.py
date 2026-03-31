import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import os

dash.register_page(__name__, path="/limpieza", name="Limpieza")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "docs", "heart_disease_health_indicators_BRFSS2015.csv"))

TITLE_STYLE = {
    "color": "#ffffff",
    "fontWeight": "800",
    "fontSize": "1.6rem",
    "borderLeft": "6px solid #C0392B",
    "paddingLeft": "14px",
    "marginBottom": "0.5rem",
    "fontFamily": "'Poppins', sans-serif"
}

SUBTITLE_STYLE = {
    "color": "#94a3b8",
    "fontSize": "0.9rem",
    "fontFamily": "'Poppins', sans-serif",
    "marginBottom": "1.5rem"
}

TEXT_STYLE = {
    "color": "#cbd5e1",
    "fontSize": "0.92rem",
    "lineHeight": "1.8",
    "fontFamily": "'Poppins', sans-serif",
    "textAlign": "justify"
}

CARD_STYLE = {
    "backgroundColor": "#0D1B2E",
    "border": "1px solid #1e3a5f",
    "borderRadius": "12px"
}

rangos = {
    "HeartDiseaseorAttack": (0, 1),
    "HighBP": (0, 1), "HighChol": (0, 1), "CholCheck": (0, 1),
    "BMI": (12, 98), "Smoker": (0, 1), "Stroke": (0, 1),
    "Diabetes": (0, 2), "PhysActivity": (0, 1), "Fruits": (0, 1),
    "Veggies": (0, 1), "HvyAlcoholConsump": (0, 1),
    "AnyHealthcare": (0, 1), "NoDocbcCost": (0, 1),
    "GenHlth": (1, 5), "MentHlth": (0, 30), "PhysHlth": (0, 30),
    "DiffWalk": (0, 1), "Sex": (0, 1), "Age": (1, 13),
    "Education": (1, 6), "Income": (1, 8),
}

continuous_vars = ["BMI", "MentHlth", "PhysHlth"]

colores = {
    "BMI": "#C0392B",
    "MentHlth": "#2C3E6B",
    "PhysHlth": "#E8A838"
}

interpretaciones = {
    "BMI": (
        "Se detectaron 9.847 valores atípicos (3.88%). Los valores extremos superiores "
        "llegan hasta 98, correspondientes a casos de obesidad mórbida severa, y los "
        "inferiores hasta 12, casos raros de desnutrición extrema. Se conservan sin modificación."
    ),
    "MentHlth": (
        "Presenta un alto porcentaje de datos atípicos (14.27%) debido a su distribución "
        "extremadamente asimétrica con mediana igual a 0. El IQR es muy pequeño (2 días). "
        "Valores como 10, 15 o 30 días son respuestas legítimas y se conservan sin tratamiento."
    ),
    "PhysHlth": (
        "Similar a MentHlth, el porcentaje de atípicos es alto (16.14%) con distribución "
        "muy asimétrica y mediana igual a 0. El IQR es de apenas 3 días. Se conservan "
        "sin tratamiento ya que son respuestas válidas de la encuesta."
    ),
}

def get_outlier_info(col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    n_out = df[(df[col] < lo) | (df[col] > hi)].shape[0]
    return {
        "Q1": round(q1, 2), "Q3": round(q3, 2), "IQR": round(iqr, 2),
        "Límite inferior": round(lo, 2), "Límite superior": round(hi, 2),
        "N° outliers": n_out,
        "% outliers": round(n_out / len(df) * 100, 2)
    }

outlier_info = {col: get_outlier_info(col) for col in continuous_vars}

# Boxplot con los 3 juntos
def make_boxplot():
    fig = go.Figure()
    for var in continuous_vars:
        fig.add_trace(go.Box(
            y=df[var],
            name=var,
            marker=dict(
                color=colores[var],
                size=4,
                opacity=0.7,
                outliercolor=colores[var],
            ),
            line=dict(color=colores[var], width=2),
            fillcolor="rgba(13,27,46,0.8)",
            boxpoints="outliers",
            jitter=0,
            whiskerwidth=0.6,
            notched=False,
        ))

    fig.update_layout(
        paper_bgcolor="#0D1B2E",
        plot_bgcolor="#0D1B2E",
        font=dict(color="#cbd5e1", family="Poppins", size=12),
        margin=dict(t=50, b=40, l=50, r=30),
        title=dict(
            text="Distribución de variables continuas",
            font=dict(color="#ffffff", size=14, family="Poppins"),
            x=0
        ),
        yaxis=dict(
            gridcolor="#1e3a5f",
            color="#94a3b8",
            zeroline=False,
        ),
        xaxis=dict(
            color="#94a3b8",
            showgrid=False,
        ),
        legend=dict(
            bgcolor="#0D1B2E",
            bordercolor="#1e3a5f",
            borderwidth=1,
            font=dict(color="#cbd5e1")
        ),
        height=480,
        showlegend=True,
    )
    return fig


layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Limpieza del Dataset", style=TITLE_STYLE),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    # Cards resumen
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("0", style={"color": "#F8F3F2", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("valores nulos", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("23.899", style={"color": "#F9F3F3", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("registros duplicados", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("9.42%", style={"color": "#EDEAEA", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("duplicados del total", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("22 / 22", style={"color": "#F5F4F4", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("variables en rango esperado", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),
    ]),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Nulos y duplicados
    dbc.Row([
        dbc.Col([
            html.H4("Valores nulos y duplicados", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "1rem"
            }),
            html.P(
                "El dataset no presenta ningún valor nulo en sus 22 variables, resultado "
                "consistente con el proceso de limpieza previo aplicado sobre el BRFSS 2015. "
                "En cuanto a los 23.899 registros duplicados (9.42%), se tomó la decisión de "
                "mantenerlos. Al tratarse de una encuesta poblacional con mayoría de variables "
                "binarias, es estadísticamente esperable que múltiples individuos compartan "
                "exactamente el mismo perfil de respuestas sin que esto represente un error "
                "de captura.",
                style=TEXT_STYLE
            ),
        ])
    ], className="mb-4"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Verificación de rangos con dropdown
    dbc.Row([
        dbc.Col([
            html.H4("Verificación de rangos esperados", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "1rem"
            }),

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown-rango",
                        options=[{"label": col, "value": col} for col in rangos.keys()],
                        value="HeartDiseaseorAttack",
                        clearable=False,
                        className="dark-dropdown",
                        style={
                            "backgroundColor": "#0D1B2E",
                            
                            "border": "1px solid #1e3a5f",
                            "borderRadius": "8px",
                            "fontFamily": "'Poppins', sans-serif",
                            "fontSize": "0.88rem"
                        }
                    ),
                ], md=4),
                dbc.Col([
                    html.Div(id="rango-resultado", style={"marginTop": "0.4rem"})
                ], md=8),
            ], className="mb-4"),
        ])
    ], className="mb-4"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Outliers — los 3 en un solo gráfico
    dbc.Row([
        dbc.Col([
            html.H4("Análisis de datos atípicos", style={
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "0.4rem"
            }),
            html.P(
                "Aplica únicamente a BMI, MentHlth y PhysHlth. "
                "Criterio de Tukey: atípico si cae fuera de Q1 − 1.5·IQR o Q3 + 1.5·IQR.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}
            ),
        ])
    ]),

    # Cards métricas de los 3
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("BMI", style={"color": "#C0392B", "fontWeight": "700",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif",
                "marginBottom": "0.8rem"}),
            html.P(f"{outlier_info['BMI']['N° outliers']:,} outliers",
                style={"textAlign": "center", "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0.2rem"}),
            html.P(f"{outlier_info['BMI']['% outliers']}% del total",
                style={"textAlign": "center", "color": "#94a3b8", "fontSize": "0.82rem", "marginBottom": "0"}),
        ]), style=CARD_STYLE), md=4, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("MentHlth", style={"color": "#2C3E6B", "fontWeight": "700",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif",
                "marginBottom": "0.8rem"}),
            html.P(f"{outlier_info['MentHlth']['N° outliers']:,} outliers",
                style={"textAlign": "center", "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0.2rem"}),
            html.P(f"{outlier_info['MentHlth']['% outliers']}% del total",
                style={"textAlign": "center", "color": "#94a3b8", "fontSize": "0.82rem", "marginBottom": "0"}),
        ]), style=CARD_STYLE), md=4, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("PhysHlth", style={"color": "#E8A838", "fontWeight": "700",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif",
                "marginBottom": "0.8rem"}),
            html.P(f"{outlier_info['PhysHlth']['N° outliers']:,} outliers",
                style={"textAlign": "center", "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0.2rem"}),
            html.P(f"{outlier_info['PhysHlth']['% outliers']}% del total",
                style={"textAlign": "center", "color": "#94a3b8", "fontSize": "0.82rem", "marginBottom": "0"}),
        ]), style=CARD_STYLE), md=4, className="mb-4"),
    ]),

    # Boxplot los 3 juntos
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(
                    figure=make_boxplot(),
                    config={"displayModeBar": False}
                )
            ]), style=CARD_STYLE)
        ])
    ], className="mb-4"),

    # Dropdown interpretación
    dbc.Row([
        dbc.Col([
            html.H5("Interpretación por variable", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "600", "marginBottom": "1rem"
            }),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="dropdown-interpretacion",
                        options=[{"label": v, "value": v} for v in continuous_vars],
                        value="BMI",
                        clearable=False,
                        className="dark-dropdown",
                        style={
                            "backgroundColor": "#0D1B2E",
                            "color": "#ffffff",
                            "border": "1px solid #1e3a5f",
                            "borderRadius": "8px",
                            "fontFamily": "'Poppins', sans-serif",
                            "fontSize": "0.88rem"
                        }
                    ),
                ], md=4),
            ], className="mb-3"),
            html.Div(id="outlier-interpretacion")
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


# Callback rango
@callback(
    Output("rango-resultado", "children"),
    Input("dropdown-rango", "value")
)
def check_rango(variable):
    min_esp, max_esp = rangos[variable]
    min_real = df[variable].min()
    max_real = df[variable].max()
    dentro = (min_real >= min_esp) and (max_real <= max_esp)

    return html.Div([
        html.Span("✓ Dentro del rango esperado" if dentro else "✗ Fuera del rango", style={
            "color": "#4CAF50" if dentro else "#C0392B",
            "fontWeight": "700",
            "fontFamily": "'Poppins', sans-serif",
            "fontSize": "0.95rem",
            "marginRight": "1.5rem"
        }),
        html.Span(f"Rango esperado: [{min_esp} – {max_esp}]", style={
            "color": "#94a3b8",
            "fontFamily": "'Poppins', sans-serif",
            "fontSize": "0.88rem",
            "marginRight": "1.5rem"
        }),
        html.Span(f"Rango real: [{min_real} – {max_real}]", style={
            "color": "#cbd5e1",
            "fontFamily": "'Poppins', sans-serif",
            "fontSize": "0.88rem"
        }),
    ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap",
              "padding": "0.6rem 1rem", "backgroundColor": "#0D1B2E",
              "borderRadius": "8px", "border": "1px solid #1e3a5f"})


# Callback interpretación
@callback(
    Output("outlier-interpretacion", "children"),
    Input("dropdown-interpretacion", "value")
)
def update_interpretacion(variable):
    return html.Div([
        html.P(interpretaciones[variable], style=TEXT_STYLE),
        html.P(
            "Decisión: No se aplica ningún tratamiento. Los valores extremos corresponden "
            "a individuos reales con perfiles de salud severos. Su exclusión introduciría "
            "un sesgo de selección que afectaría la validez del análisis.",
            style={**TEXT_STYLE, "color": "#94a3b8", "fontStyle": "italic",
                   "marginTop": "0.5rem", "marginBottom": "0"}
        )
    ], style={
        "padding": "1rem 1.2rem",
        "backgroundColor": "#0D1B2E",
        "borderLeft": "4px solid #C0392B",
        "borderRadius": "8px",
        "border": "1px solid #1e3a5f"
    })