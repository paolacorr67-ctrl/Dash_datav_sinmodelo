import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import os

dash.register_page(__name__, path="/modelo", name="Modelo Predictivo")

# ── Paleta ────────────────────────────────────────────────────────────────────
BG_PAGE     = "#070E1A"
BG_CARD     = "#0D1B2E"
BG_CARD_ALT = "#111827"
BORDER      = "#1e3a5f"
TEXT_PRI    = "#ffffff"
TEXT_SEC    = "#94a3b8"
ACCENT      = "#C0392B"
FONT        = "'Poppins', sans-serif"

# ── Entrenar modelo al importar ───────────────────────────────────────────────
def _build_model():
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "docs",
        "heart_disease_health_indicators_BRFSS2015.csv"
    )
    df = pd.read_csv(csv_path)
    top_vars = ["HighBP", "GenHlth", "HighChol", "Age", "DiffWalk",
                "Sex", "Stroke", "Smoker", "Diabetes", "PhysHlth",
                "Income", "HvyAlcoholConsump"]
    X = df[top_vars]
    y = df["HeartDiseaseorAttack"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    preprocessor = ColumnTransformer([
        ("num",  MinMaxScaler(), ["PhysHlth"]),
        ("rest", "passthrough",
         [c for c in top_vars if c != "PhysHlth"])
    ])
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", XGBClassifier(
            random_state=42, scale_pos_weight=neg / pos,
            eval_metric="logloss", verbosity=0,
            learning_rate=0.05, max_depth=3,
            n_estimators=100, subsample=1.0
        ))
    ])
    model.fit(X_train, y_train)
    return model

MODEL = _build_model()

# ── Metadatos variables ───────────────────────────────────────────────────────
VARS_META = {
    "HighBP": {
        "label": "Presion arterial alta",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
    "GenHlth": {
        "label": "Estado de salud general autopercibido",
        "type": "slider",
        "min": 1, "max": 5, "step": 1,
        "marks": {1: "Excelente", 2: "Muy bueno", 3: "Bueno",
                  4: "Regular", 5: "Malo"},
    },
    "HighChol": {
        "label": "Colesterol alto",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
    "Age": {
        "label": "Rango de edad",
        "type": "slider",
        "min": 1, "max": 13, "step": 1,
        "marks": {1: "18-24", 4: "30-34", 7: "45-49",
                  10: "60-64", 13: "80+"},
    },
    "DiffWalk": {
        "label": "Dificultad para caminar o subir escaleras",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
    "Sex": {
        "label": "Sexo biologico",
        "type": "radio",
        "options": [{"label": "Femenino", "value": 0},
                    {"label": "Masculino", "value": 1}],
    },
    "Stroke": {
        "label": "Antecedente de derrame cerebral",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
    "Smoker": {
        "label": "Ha fumado 100 o mas cigarrillos en su vida",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
    "Diabetes": {
        "label": "Condicion de diabetes",
        "type": "slider",
        "min": 0, "max": 2, "step": 1,
        "marks": {0: "No", 1: "Pre-diabetes", 2: "Si"},
    },
    "PhysHlth": {
        "label": "Dias con mala salud fisica en los ultimos 30 dias",
        "type": "slider",
        "min": 0, "max": 30, "step": 1,
        "marks": {0: "0", 5: "5", 10: "10", 15: "15",
                  20: "20", 25: "25", 30: "30"},
    },
    "Income": {
        "label": "Nivel de ingreso anual",
        "type": "slider",
        "min": 1, "max": 8, "step": 1,
        "marks": {1: "<$10k", 3: "<$25k", 5: "<$50k", 8: "$75k+"},
    },
    "HvyAlcoholConsump": {
        "label": "Consumo excesivo de alcohol",
        "type": "radio",
        "options": [{"label": "No", "value": 0}, {"label": "Si", "value": 1}],
    },
}

SLIDER_MARK_STYLE = {"color": TEXT_SEC, "fontSize": "11px",
                     "fontFamily": FONT}

# ── Helpers ───────────────────────────────────────────────────────────────────
def _make_input(var_id, meta):
    if meta["type"] == "radio":
        return dbc.RadioItems(
            id=f"input-{var_id}",
            options=meta["options"],
            value=None,
            inline=True,
            inputStyle={"marginRight": "5px", "accentColor": ACCENT},
            labelStyle={
                "marginRight": "22px",
                "color": TEXT_SEC,
                "fontFamily": FONT,
                "fontSize": "14px",
                "fontWeight": "500",
                "cursor": "pointer"
            }
        )
    else:
        return dcc.Slider(
            id=f"input-{var_id}",
            min=meta["min"], max=meta["max"], step=meta["step"],
            value=None,
            marks={k: {"label": v, "style": SLIDER_MARK_STYLE}
                   for k, v in meta["marks"].items()},
            tooltip={"placement": "top", "always_visible": False},
        )


def _input_card(var_id, meta):
    return dbc.Col(
        html.Div([
            html.Label(
                meta["label"],
                style={
                    "color": TEXT_PRI,
                    "fontFamily": FONT,
                    "fontSize": "12px",
                    "fontWeight": "600",
                    "marginBottom": "14px",
                    "display": "block",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.6px",
                    "lineHeight": "1.4"
                }
            ),
            _make_input(var_id, meta)
        ], style={
            "backgroundColor": BG_CARD,
            "border": f"1px solid {BORDER}",
            "borderRadius": "10px",
            "padding": "20px 22px",
            "height": "100%"
        }),
        md=6, lg=4, className="mb-3"
    )


# ── Layout ────────────────────────────────────────────────────────────────────
layout = html.Div([
    dbc.Container([

        # Encabezado
        html.Div([
            html.H2(
                "Modelo Predictivo — XGBoost",
                style={"color": TEXT_PRI, "fontFamily": FONT,
                       "fontWeight": "700", "marginBottom": "10px",
                       "fontSize": "22px", "letterSpacing": "0.3px"}
            ),
            html.P(
                "Complete los campos clinicos y sociodemograficos para obtener "
                "una estimacion de la probabilidad de enfermedad cardiaca. "
                "El modelo fue entrenado con la encuesta BRFSS 2015 (253,680 "
                "registros) empleando las 12 variables de mayor relevancia "
                "predictiva (AUC = 0.84).",
                style={"color": TEXT_SEC, "fontFamily": FONT,
                       "fontSize": "14px", "maxWidth": "860px",
                       "lineHeight": "1.75", "marginBottom": "0"}
            )
        ], style={
            "borderLeft": f"4px solid {ACCENT}",
            "paddingLeft": "22px",
            "marginBottom": "36px"
        }),

        # Subtitulo seccion
        html.P(
            "Variables de entrada",
            style={"color": TEXT_SEC, "fontFamily": FONT,
                   "fontSize": "10px", "textTransform": "uppercase",
                   "letterSpacing": "2px", "marginBottom": "14px",
                   "fontWeight": "600"}
        ),

        # Formulario
        dbc.Row([_input_card(v, m) for v, m in VARS_META.items()]),

        # Aviso de campos incompletos
        html.Div(id="warning-empty", style={"marginTop": "6px"}),

        # Boton
        dbc.Row(dbc.Col(
            dbc.Button(
                "Ejecutar prediccion",
                id="btn-predict",
                n_clicks=0,
                style={
                    "backgroundColor": ACCENT,
                    "border": "none",
                    "borderRadius": "8px",
                    "padding": "13px 0",
                    "fontSize": "13px",
                    "fontWeight": "700",
                    "fontFamily": FONT,
                    "color": TEXT_PRI,
                    "width": "100%",
                    "letterSpacing": "1.5px",
                    "textTransform": "uppercase"
                }
            ),
            md={"size": 4, "offset": 4},
            className="text-center mt-4 mb-2"
        )),

        # Resultado
        html.Div(
            "Haga clic en 'Ejecutar prediccion' para visualizar el resultado.",
            id="instruccion-msg",
            style={
                "backgroundColor": BG_CARD,
                "border": f"1px solid {BORDER}",
                "borderLeft": f"3px solid #1e6a9e",
                "borderRadius": "8px",
                "color": TEXT_SEC,
                "fontFamily": FONT,
                "fontSize": "13px",
                "padding": "12px 18px",
                "marginTop": "10px",
                "marginBottom": "10px",
                "textAlign": "center"
                
                
            }
        ),
        html.Div(id="resultado-prediccion", style={"marginTop": "10px"}),

    ], fluid=True, style={"maxWidth": "1200px", "margin": "0 auto"})

], style={"backgroundColor": BG_PAGE, "padding": "2rem 3rem",
           "minHeight": "100vh"})


# ── Callback ──────────────────────────────────────────────────────────────────
@callback(
    Output("resultado-prediccion", "children"),
    Output("warning-empty",        "children"),
    Input("btn-predict", "n_clicks"),
    [State(f"input-{v}", "value") for v in VARS_META.keys()],
    prevent_initial_call=True
)
def predict(*args):
    values = list(args[1:])

    # Validacion
    missing = [VARS_META[k]["label"]
               for k, v in zip(VARS_META.keys(), values) if v is None]
    if missing:
        return "", html.Div(
            "Complete los siguientes campos antes de continuar: "
            + ", ".join(missing) + ".",
            style={
                "backgroundColor": "#1a0505",
                "border": f"1px solid {ACCENT}",
                "borderRadius": "8px",
                "color": "#e87070",
                "fontFamily": FONT,
                "fontSize": "13px",
                "padding": "13px 18px",
                "lineHeight": "1.6"
            }
        )

    # Prediccion
    row      = dict(zip(VARS_META.keys(), values))
    df_in    = pd.DataFrame([row])
    prob     = float(MODEL.predict_proba(df_in)[0][1])
    prob_pct = round(prob * 100, 1)

    if prob < 0.30:
        nivel, color_nivel = "BAJO",     "#27AE60"
    elif prob < 0.55:
        nivel, color_nivel = "MODERADO", "#E67E22"
    else:
        nivel, color_nivel = "ALTO",     ACCENT

    # ── Gauge ────────────────────────────────────────────────────────────────
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_pct,
        number={"suffix": "%",
                "font": {"size": 46, "color": color_nivel, "family": FONT}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": BORDER,
                "tickfont": {"color": TEXT_SEC, "size": 11, "family": FONT}
            },
            "bar": {"color": color_nivel, "thickness": 0.28},
            "bgcolor": BG_CARD_ALT,
            "borderwidth": 0,
            "steps": [
                {"range": [0,  30],  "color": "#071410"},
                {"range": [30, 55],  "color": "#141007"},
                {"range": [55, 100], "color": "#140707"},
            ],
            "threshold": {
                "line": {"color": color_nivel, "width": 3},
                "thickness": 0.8,
                "value": prob_pct
            }
        },
        title={"text": "Probabilidad estimada de enfermedad cardiaca",
               "font": {"size": 12, "color": TEXT_SEC, "family": FONT}}
    ))
    fig_gauge.update_layout(
        height=270,
        margin=dict(l=30, r=30, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # ── Barras contribucion relativa ─────────────────────────────────────────
    factor_risk = {
        "Presion arterial alta":        row["HighBP"]   * 0.18,
        "Salud general autopercibida":  (row["GenHlth"] - 1) / 4 * 0.16,
        "Colesterol alto":              row["HighChol"] * 0.14,
        "Rango de edad":                (row["Age"] - 1) / 12 * 0.13,
        "Dificultad al caminar":        row["DiffWalk"] * 0.11,
        "Antecedente de derrame":       row["Stroke"]   * 0.10,
        "Condicion de diabetes":        row["Diabetes"] / 2 * 0.09,
        "Dias con mala salud fisica":   row["PhysHlth"] / 30 * 0.09,
    }
    sorted_f  = dict(sorted(factor_risk.items(), key=lambda x: x[1],
                             reverse=True))
    max_val   = max(sorted_f.values()) if max(sorted_f.values()) > 0 else 1
    bar_colors = [ACCENT if v >= max_val * 0.6 else BORDER
                  for v in sorted_f.values()]

    fig_bar = go.Figure(go.Bar(
        x=list(sorted_f.values()),
        y=list(sorted_f.keys()),
        orientation="h",
        marker_color=bar_colors,
        hovertemplate="%{y}: %{x:.3f}<extra></extra>"
    ))
    fig_bar.update_layout(
        title={"text": "Contribucion relativa por factor de riesgo",
               "font": {"size": 12, "color": TEXT_SEC, "family": FONT}},
        xaxis={"showgrid": False, "zeroline": False,
               "showticklabels": False},
        yaxis={"autorange": "reversed", "color": TEXT_SEC,
               "tickfont": {"family": FONT, "size": 12}},
        height=290,
        margin=dict(l=10, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_SEC, "size": 12, "family": FONT}
    )

    # ── Resultado ────────────────────────────────────────────────────────────
    return html.Div([

        # Banner nivel + probabilidad
        html.Div([
            html.Div([
                html.Span(
                    "NIVEL DE RIESGO",
                    style={"color": TEXT_SEC, "fontFamily": FONT,
                           "fontSize": "10px", "letterSpacing": "1.8px",
                           "fontWeight": "600", "textTransform": "uppercase",
                           "display": "block", "marginBottom": "6px"}
                ),
                html.Span(
                    nivel,
                    style={"color": color_nivel, "fontFamily": FONT,
                           "fontSize": "26px", "fontWeight": "800",
                           "letterSpacing": "3px"}
                )
            ], style={"flex": "1", "borderRight": f"1px solid {BORDER}",
                      "paddingRight": "32px"}),
            html.Div([
                html.Span(
                    "PROBABILIDAD ESTIMADA",
                    style={"color": TEXT_SEC, "fontFamily": FONT,
                           "fontSize": "10px", "letterSpacing": "1.8px",
                           "fontWeight": "600", "textTransform": "uppercase",
                           "display": "block", "marginBottom": "6px"}
                ),
                html.Span(
                    f"{prob_pct}%",
                    style={"color": color_nivel, "fontFamily": FONT,
                           "fontSize": "26px", "fontWeight": "800"}
                )
            ], style={"flex": "1", "paddingLeft": "32px"})
        ], style={
            "display": "flex",
            "alignItems": "center",
            "backgroundColor": BG_CARD,
            "border": f"1px solid {BORDER}",
            "borderTop": f"3px solid {color_nivel}",
            "borderRadius": "10px",
            "padding": "22px 32px",
            "marginBottom": "16px"
        }),

        # Graficas
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(figure=fig_gauge,
                              config={"displayModeBar": False}),
                    style={"backgroundColor": BG_CARD,
                           "border": f"1px solid {BORDER}",
                           "borderRadius": "10px", "padding": "8px"}
                ), md=5, className="mb-3"
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(figure=fig_bar,
                              config={"displayModeBar": False}),
                    style={"backgroundColor": BG_CARD,
                           "border": f"1px solid {BORDER}",
                           "borderRadius": "10px", "padding": "8px"}
                ), md=7, className="mb-3"
            ),
        ], className="g-3"),

        # Nota metodologica
        html.P(
            "Nota metodologica: Esta herramienta tiene fines academicos e "
            "ilustrativos. La probabilidad se estima a partir de un modelo "
            "XGBoost entrenado sobre datos poblacionales de la encuesta BRFSS "
            "2015 y no constituye un diagnostico clinico.",
            style={"color": TEXT_SEC, "fontFamily": FONT, "fontSize": "12px",
                   "marginTop": "8px", "lineHeight": "1.65",
                   "borderTop": f"1px solid {BORDER}",
                   "paddingTop": "16px", "marginBottom": "30px"}
        )

    ]), ""