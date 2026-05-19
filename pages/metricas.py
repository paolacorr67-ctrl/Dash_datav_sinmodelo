import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path="/metricas", name="Métricas")

# ── Paleta ────────────────────────────────────────────────────────────────────
BG_PAGE     = "#070E1A"
BG_CARD     = "#0D1B2E"
BG_CARD_ALT = "#111827"
BORDER      = "#1e3a5f"
TEXT_PRI    = "#ffffff"
TEXT_SEC    = "#94a3b8"
TEXT_MUT    = "#cbd5e1"
ACCENT      = "#C0392B"
GOLD        = "#E8A838"
BLUE        = "#2C3E6B"
FONT        = "'Poppins', sans-serif"

TITLE_STYLE = {
    "color": TEXT_PRI, "fontWeight": "800", "fontSize": "1.6rem",
    "borderLeft": f"6px solid {ACCENT}", "paddingLeft": "14px",
    "marginBottom": "0.5rem", "fontFamily": FONT
}
SUBTITLE_STYLE = {
    "color": TEXT_SEC, "fontSize": "0.9rem",
    "fontFamily": FONT, "marginBottom": "1rem"
}
TEXT_STYLE = {
    "color": TEXT_MUT, "fontSize": "0.92rem", "lineHeight": "1.8",
    "fontFamily": FONT, "textAlign": "justify"
}
CARD_STYLE = {
    "backgroundColor": BG_CARD,
    "border": f"1px solid {BORDER}",
    "borderRadius": "12px"
}
PLOT_BASE = dict(
    paper_bgcolor=BG_CARD,
    plot_bgcolor=BG_CARD,
    font=dict(color=TEXT_MUT, family="Poppins", size=12),
    margin=dict(t=50, b=50, l=50, r=30),
)

# ── Datos ─────────────────────────────────────────────────────────────────────
modelos = pd.DataFrame([
    {"Modelo": "XGBoost",       "Accuracy": 0.7351, "Precision": 0.2376,
     "Recall": 0.8209, "F1": 0.3686, "AUC-ROC": 0.8483, "Recall CV": 0.8197},
    {"Modelo": "Random Forest", "Accuracy": 0.7237, "Precision": 0.2288,
     "Recall": 0.8157, "F1": 0.3574, "AUC-ROC": 0.8373, "Recall CV": 0.8102},
    {"Modelo": "Logistic Reg.", "Accuracy": 0.7502, "Precision": 0.2458,
     "Recall": 0.7991, "F1": 0.3760, "AUC-ROC": 0.8459, "Recall CV": 0.7960},
    {"Modelo": "KNeighbors",    "Accuracy": 0.8815, "Precision": 0.2944,
     "Recall": 0.1846, "F1": 0.2269, "AUC-ROC": 0.6690, "Recall CV": 0.1947},
    {"Modelo": "Linear SVC",    "Accuracy": 0.9070, "Precision": 0.5262,
     "Recall": 0.1241, "F1": 0.2008, "AUC-ROC": 0.8460, "Recall CV": 0.1290},
])

reduccion = pd.DataFrame([
    {"Modelo": "XGBoost completo (21 vars)",  "Variables": 21,
     "Recall": 0.8209, "Precision": 0.2376, "F1": 0.3686, "AUC-ROC": 0.8483},
    {"Modelo": "XGBoost reducido A (16 vars)", "Variables": 16,
     "Recall": 0.8209, "Precision": 0.2376, "F1": 0.3686, "AUC-ROC": 0.8483},
    {"Modelo": "XGBoost reducido B (12 vars)", "Variables": 12,
     "Recall": 0.8223, "Precision": 0.2376, "F1": 0.3687, "AUC-ROC": 0.8482},
])

vars_eliminadas = {
    "Importancia = 0":     ["Veggies", "PhysActivity", "Fruits", "Education", "AnyHealthcare"],
    "Importancia < 0.003": ["CholCheck", "BMI", "NoDocbcCost", "MentHlth"],
}

vars_finales = ["HighBP", "GenHlth", "HighChol", "Age", "DiffWalk",
                "Sex", "Stroke", "Smoker", "Diabetes", "PhysHlth",
                "Income", "HvyAlcoholConsump"]

# ── Matrices de confusión (datos hardcodeados del notebook) ──────────────────
cms = {
    "Logistic Reg.": {"TN": 34242, "FP": 11715, "FN": 960,  "TP": 3819},
    "Random Forest":  {"TN": 32819, "FP": 13138, "FN": 881,  "TP": 3898},
    "KNeighbors":     {"TN": 43843, "FP": 2114,  "FN": 3897, "TP": 882},
    "Linear SVC":     {"TN": 45423, "FP": 534,   "FN": 4186, "TP": 593},
    "XGBoost":        {"TN": 33372, "FP": 12585, "FN": 856,  "TP": 3923},
}

def make_cm_figure(nombre, vals):
    z     = [[vals["TN"], vals["FP"]],
             [vals["FN"], vals["TP"]]]
    text  = [[f"TN<br>{vals['TN']:,}", f"FP<br>{vals['FP']:,}"],
             [f"FN<br>{vals['FN']:,}", f"TP<br>{vals['TP']:,}"]]

    fig = go.Figure(go.Heatmap(
        z=z,
        text=text,
        texttemplate="%{text}",
        colorscale=[[0, BG_CARD_ALT], [0.3, "#7B241C"], [1, ACCENT]],
        showscale=False,
        xgap=3, ygap=3,
        textfont=dict(color=TEXT_PRI, family=FONT, size=11)
    ))
    fig.update_layout(
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(color=TEXT_MUT, family="Poppins", size=12),
        margin=dict(t=50, b=50, l=60, r=20),
        height=260,
        title=dict(
            text=nombre,
            font=dict(color=TEXT_PRI, size=13, family=FONT),
            x=0.5
        ),
        xaxis=dict(
            tickvals=[0, 1],
            ticktext=["Sin HD", "Con HD"],
            color=TEXT_SEC,
            title=dict(text="Prediccion", font=dict(size=11, color=TEXT_SEC))
        ),
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=["Sin HD", "Con HD"],
            color=TEXT_SEC,
            autorange="reversed",
            title=dict(text="Real", font=dict(size=11, color=TEXT_SEC))
        ),
    )
    return fig

# ── Gráfica 1: Comparación de modelos ────────────────────────────────────────
fig_comp = go.Figure()
colors_bar = [ACCENT if m == "XGBoost" else BLUE for m in modelos["Modelo"]]

fig_comp.add_trace(go.Bar(
    name="Recall",
    x=modelos["Modelo"],
    y=modelos["Recall"],
    marker_color=colors_bar,
    text=[f"{v:.3f}" for v in modelos["Recall"]],
    textposition="outside",
    textfont=dict(color=TEXT_MUT, size=11),
))
fig_comp.add_trace(go.Scatter(
    name="AUC-ROC",
    x=modelos["Modelo"],
    y=modelos["AUC-ROC"],
    mode="lines+markers",
    line=dict(color=GOLD, width=2),
    marker=dict(color=GOLD, size=8),
    yaxis="y2"
))
fig_comp.update_layout(
    **PLOT_BASE,
    title=dict(text="Recall y AUC-ROC por modelo",
               font=dict(color=TEXT_PRI, size=14, family=FONT), x=0),
    xaxis=dict(gridcolor=BORDER, color=TEXT_SEC),
    yaxis=dict(gridcolor=BORDER, color=TEXT_SEC, title="Recall",
               range=[0, 1.15]),
    yaxis2=dict(overlaying="y", side="right", color=GOLD,
                title="AUC-ROC", range=[0.5, 1.0], showgrid=False),
    legend=dict(bgcolor=BG_CARD, bordercolor=BORDER, borderwidth=1,
                font=dict(color=TEXT_MUT)),
    height=380, barmode="group",
)

# ── Gráfica 2: Tabla comparativa ──────────────────────────────────────────────
header_vals = ["Modelo", "Accuracy", "Precision", "Recall", "F1", "AUC-ROC", "Recall CV"]
cell_vals   = [
    modelos["Modelo"].tolist(),
    [f"{v:.4f}" for v in modelos["Accuracy"]],
    [f"{v:.4f}" for v in modelos["Precision"]],
    [f"{v:.4f}" for v in modelos["Recall"]],
    [f"{v:.4f}" for v in modelos["F1"]],
    [f"{v:.4f}" for v in modelos["AUC-ROC"]],
    [f"{v:.4f}" for v in modelos["Recall CV"]],
]
row_colors = [
    [ACCENT if m == "XGBoost" else BG_CARD_ALT for m in modelos["Modelo"]]
] * len(header_vals)

fig_tabla = go.Figure(go.Table(
    header=dict(values=header_vals, fill_color=BORDER,
                font=dict(color=TEXT_PRI, family=FONT, size=12),
                align="center", height=36),
    cells=dict(values=cell_vals, fill_color=row_colors,
               font=dict(color=TEXT_MUT, family=FONT, size=12),
               align="center", height=32,
               line=dict(color=BORDER, width=1))
))
fig_tabla.update_layout(
    paper_bgcolor=BG_CARD,
    margin=dict(t=10, b=10, l=10, r=10),
    height=240
)

# ── Gráfica 3: Reducción de variables ────────────────────────────────────────
fig_red = go.Figure()
metrics = ["Recall", "F1", "AUC-ROC"]
pal     = [ACCENT, GOLD, "#4A6FA5"]

for met, col in zip(metrics, pal):
    fig_red.add_trace(go.Bar(
        name=met, x=reduccion["Modelo"], y=reduccion[met],
        marker_color=col,
        text=[f"{v:.4f}" for v in reduccion[met]],
        textposition="outside",
        textfont=dict(color=TEXT_MUT, size=10),
    ))
fig_red.update_layout(
    **PLOT_BASE,
    title=dict(text="Comparacion de versiones XGBoost por numero de variables",
               font=dict(color=TEXT_PRI, size=14, family=FONT), x=0),
    xaxis=dict(gridcolor=BORDER, color=TEXT_SEC),
    yaxis=dict(gridcolor=BORDER, color=TEXT_SEC, title="Metrica", range=[0, 1.1]),
    legend=dict(bgcolor=BG_CARD, bordercolor=BORDER, borderwidth=1,
                font=dict(color=TEXT_MUT)),
    barmode="group", height=380,
)

# ── Helpers UI ────────────────────────────────────────────────────────────────
def metric_card(label, value, color=TEXT_PRI, highlight=False):
    return dbc.Col(
        dbc.Card(dbc.CardBody([
            html.P(label, style={"color": TEXT_SEC, "fontSize": "0.78rem",
                                  "fontFamily": FONT, "marginBottom": "0.4rem",
                                  "textTransform": "uppercase",
                                  "letterSpacing": "0.8px"}),
            html.H4(value, style={"color": TEXT_PRI, "fontWeight": "800",
                                   "fontFamily": FONT, "marginBottom": "0"})
        ]), style={**CARD_STYLE, "borderColor": ACCENT if highlight else BORDER}),
        md=3, className="mb-3"
    )

def section_title(text):
    return html.H4(text, style={"color": TEXT_PRI, "fontFamily": FONT,
                                 "fontWeight": "700", "marginBottom": "0.3rem"})

# ── Layout ────────────────────────────────────────────────────────────────────
layout = dbc.Container([

    dbc.Row([dbc.Col([
        html.H1("Seleccion y evaluacion del modelo", style=TITLE_STYLE),
        html.P("Comparacion de cinco algoritmos de clasificacion y justificacion "
               "de la seleccion del modelo XGBoost con 12 variables.",
               style={**SUBTITLE_STYLE, "marginBottom": "0"}),
        html.Hr(style={"borderColor": BORDER, "marginTop": "1rem"}),
    ])], className="mt-4"),

    # ── SECCION 1: Comparacion de modelos ─────────────────────────────────────
    dbc.Row([dbc.Col([
        section_title("1. Comparacion de modelos"),
        html.P("Se entrenaron cinco algoritmos con validacion cruzada estratificada "
               "(5 folds), aplicando ajuste de pesos de clase para compensar el "
               "desbalance de clases (90.6% vs 9.4%). El criterio principal de "
               "seleccion fue el Recall sobre la clase positiva, dado que en un "
               "contexto clinico es preferible minimizar los falsos negativos.",
               style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}),
    ])]),

    dbc.Row([
        metric_card("Recall",    "0.8209", ACCENT, highlight=True),
        metric_card("AUC-ROC",   "0.8483", GOLD),
        metric_card("F1-Score",  "0.3686", "#4A6FA5"),
        metric_card("Recall CV", "0.8197", TEXT_PRI),
    ]),

    dbc.Row([dbc.Col([
        dbc.Card(dbc.CardBody([
            dcc.Graph(figure=fig_tabla, config={"displayModeBar": False})
        ]), style=CARD_STYLE)
    ])], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=fig_comp, config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=8),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H6("Por que XGBoost?", style={"color": TEXT_PRI,
                    "fontFamily": FONT, "fontWeight": "700",
                    "marginBottom": "1rem",
                    "borderBottom": f"1px solid {BORDER}",
                    "paddingBottom": "0.5rem"}),
                html.P("XGBoost obtuvo el Recall mas alto (0.8209) junto con el "
                       "AUC-ROC mas elevado (0.8483), lo que lo posiciona como el "
                       "modelo con mayor capacidad para detectar casos reales de "
                       "enfermedad cardiaca.",
                       style={**TEXT_STYLE, "marginBottom": "1rem"}),
                html.P("KNeighbors y Linear SVC alcanzaron una Accuracy superior "
                       "(0.88 y 0.91), pero con un Recall de apenas 0.18 y 0.12 "
                       "respectivamente, lo que significa que detectan menos de 1 "
                       "de cada 5 casos positivos. En un contexto clinico, esta "
                       "metrica es inaceptable.",
                       style={**TEXT_STYLE, "marginBottom": "1rem"}),
                html.P("Logistic Regression obtuvo un F1 ligeramente superior "
                       "(0.376 vs 0.369), pero un AUC-ROC y Recall CV inferiores, "
                       "lo que indica menor estabilidad en validacion cruzada.",
                       style={**TEXT_STYLE, "marginBottom": "0"}),
            ]), style={**CARD_STYLE, "height": "100%"})
        ], md=4),
    ], className="mb-5", style={"alignItems": "stretch"}),

    html.Hr(style={"borderColor": BORDER}),

    # ── SECCION 2: Matrices de confusion ──────────────────────────────────────
    dbc.Row([dbc.Col([
        section_title("2. Matrices de confusion por modelo"),
        html.P("Las matrices de confusion permiten visualizar el comportamiento "
               "de cada modelo frente a los casos positivos y negativos. "
               "En este problema, los falsos negativos (FN) son el error mas "
               "critico: representan pacientes enfermos que el modelo no detecto.",
               style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}),
    ])]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_cm_figure("XGBoost", cms["XGBoost"]),
                          config={"displayModeBar": False})
            ]), style={**CARD_STYLE, "borderColor": ACCENT})
        ], md=4, className="mb-3"),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_cm_figure("Random Forest", cms["Random Forest"]),
                          config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=4, className="mb-3"),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_cm_figure("Logistic Reg.", cms["Logistic Reg."]),
                          config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=4, className="mb-3"),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_cm_figure("KNeighbors", cms["KNeighbors"]),
                          config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=4, className="mb-3"),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_cm_figure("Linear SVC", cms["Linear SVC"]),
                          config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=4, className="mb-3"),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H6("Interpretacion", style={"color": TEXT_PRI,
                    "fontFamily": FONT, "fontWeight": "700",
                    "marginBottom": "1rem",
                    "borderBottom": f"1px solid {BORDER}",
                    "paddingBottom": "0.5rem"}),
                html.P("XGBoost registro el menor numero de falsos negativos (856)"
                       "entre todos los modelos evaluados, detectando 3.923 de los"
                       "4.779 casos positivos reales en el conjunto de test.",
                       style={**TEXT_STYLE, "marginBottom": "1rem"}),
                html.P("Random Forest obtuvo resultados similares (FN: 881, TP: 3.898), "
                       "pero con un AUC-ROC inferior (0.837 vs 0.848),lo que indica "
                       "menor capacidad discriminatoria global.",
                       style={**TEXT_STYLE, "marginBottom": "1rem"}),           
            ]), style={**CARD_STYLE, "height": "100%"})
        ], md=4, className="mb-3"),
    ], style={"alignItems": "stretch"}),

    html.Hr(style={"borderColor": BORDER, "marginTop": "1rem"}),

    # ── SECCION 3: Reduccion de variables ─────────────────────────────────────
    dbc.Row([dbc.Col([
        section_title("3. Reduccion a 12 variables"),
        html.P("Con el objetivo de construir un modelo mas parsimonioso sin "
               "sacrificar capacidad predictiva, se analizo la importancia de "
               "variables del XGBoost entrenado con las 21 variables del dataset.",
               style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}),
    ])]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.P("IMPORTANCIA = 0", style={"color": TEXT_SEC,
                    "fontSize": "10px", "letterSpacing": "1.5px",
                    "fontFamily": FONT, "fontWeight": "600",
                    "textTransform": "uppercase", "marginBottom": "12px"}),
                html.P("El algoritmo no las utilizo en ningun arbol de decision "
                       "durante el entrenamiento.",
                       style={"color": TEXT_MUT, "fontFamily": FONT,
                              "fontSize": "12px", "marginBottom": "12px"}),
                html.Div([
                    html.Span(v, style={
                        "backgroundColor": BG_CARD_ALT,
                        "border": f"1px solid {BORDER}",
                        "borderRadius": "4px",
                        "color": TEXT_SEC,
                        "fontFamily": FONT,
                        "fontSize": "12px",
                        "padding": "3px 10px",
                        "marginRight": "6px",
                        "marginBottom": "6px",
                        "display": "inline-block"
                    }) for v in vars_eliminadas["Importancia = 0"]
                ])
            ]), style={**CARD_STYLE, "borderLeft": f"3px solid {BORDER}"}),
        ], md=6, className="mb-3"),

        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.P("IMPORTANCIA < 0.003", style={"color": TEXT_SEC,
                    "fontSize": "10px", "letterSpacing": "1.5px",
                    "fontFamily": FONT, "fontWeight": "600",
                    "textTransform": "uppercase", "marginBottom": "12px"}),
                html.P("Contribucion marginal al poder predictivo del modelo.",
                       style={"color": TEXT_MUT, "fontFamily": FONT,
                              "fontSize": "12px", "marginBottom": "12px"}),
                html.Div([
                    html.Span(v, style={
                        "backgroundColor": BG_CARD_ALT,
                        "border": f"1px solid {BORDER}",
                        "borderRadius": "4px",
                        "color": TEXT_SEC,
                        "fontFamily": FONT,
                        "fontSize": "12px",
                        "padding": "3px 10px",
                        "marginRight": "6px",
                        "marginBottom": "6px",
                        "display": "inline-block"
                    }) for v in vars_eliminadas["Importancia < 0.003"]
                ])
            ]), style={**CARD_STYLE, "borderLeft": f"3px solid {BORDER}"}),
        ], md=6, className="mb-3"),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=fig_red, config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=7),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H6("Resultado de la comparacion", style={"color": TEXT_PRI,
                    "fontFamily": FONT, "fontWeight": "700",
                    "marginBottom": "1rem",
                    "borderBottom": f"1px solid {BORDER}",
                    "paddingBottom": "0.5rem"}),
                html.P("Las tres versiones del modelo obtuvieron metricas "
                       "practicamente identicas: Recall de 0.8209, 0.8209 y "
                       "0.8223 respectivamente, y AUC-ROC de 0.8483, 0.8483 "
                       "y 0.8482.",
                       style={**TEXT_STYLE, "marginBottom": "1rem"}),
                html.P("Esto confirma que las 9 variables eliminadas no aportaban "
                       "informacion predictiva relevante. Se selecciono el modelo "
                       "reducido B como modelo final por ser el mas simple, "
                       "interpretable y eficiente.",
                       style={**TEXT_STYLE, "marginBottom": "0"}),
            ]), style={**CARD_STYLE, "height": "100%"})
        ], md=5),
    ], className="mb-4", style={"alignItems": "stretch"}),

    dbc.Row([dbc.Col([
        dbc.Card(dbc.CardBody([
            html.P("12 VARIABLES SELECCIONADAS", style={"color": TEXT_SEC,
                "fontSize": "10px", "letterSpacing": "1.5px",
                "fontFamily": FONT, "fontWeight": "600",
                "textTransform": "uppercase", "marginBottom": "14px"}),
            html.Div([
                html.Span(v, style={
                    "backgroundColor": "#0d2137",
                    "border": f"1px solid {BORDER}",
                    "borderRadius": "6px",
                    "color": TEXT_PRI,
                    "fontFamily": FONT,
                    "fontSize": "13px",
                    "fontWeight": "600",
                    "padding": "10px 12px",
                    "marginRight": "6px",
                    "textAlign": "center",
                    "marginBottom": "8px",
                    "display": "inline-block",
                }) for v in vars_finales
            ])
        ]), style={**CARD_STYLE, "borderLeft": f"3px solid {ACCENT}"})
    ])], className="mb-5"),

    html.Hr(style={"borderColor": BORDER}),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": BG_PAGE})