import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/referencias", name="Referencias")

TITLE_STYLE = {
    "color": "#ffffff", "fontWeight": "800", "fontSize": "1.6rem",
    "borderLeft": "6px solid #C0392B", "paddingLeft": "14px",
    "marginBottom": "0.5rem", "fontFamily": "'Poppins', sans-serif"
}
CARD_STYLE = {
    "backgroundColor": "#0D1B2E", "border": "1px solid #1e3a5f", "borderRadius": "12px"
}

referencias = [
    {
        "titulo": "Heart Disease Health Indicators Dataset — BRFSS 2015",
        "detalle": "Alex Teboul · Kaggle · 2021",
        "url": "https://www.kaggle.com/datasets/alexteboul/heart-disease-health-indicators-dataset",
    },
    {
        "titulo": "Behavioral Risk Factor Surveillance System (BRFSS) — 2015",
        "detalle": "Centers for Disease Control and Prevention (CDC) · 2015",
        "url": "https://www.cdc.gov/brfss/annual_data/annual_2015.html",
    },
    {
        "titulo": "Heart Disease Facts",
        "detalle": "Centers for Disease Control and Prevention (CDC) · 2023",
        "url": "https://www.cdc.gov/heartdisease/facts.htm",
    },
    {
        "titulo": "Americans under 55 dying of severe heart attacks",
        "detalle": "American Heart Association · Journal of the American Heart Association · 2024",
        "url": "https://www.ahajournals.org",
    },
    {
        "titulo": "Ataque cardíaco: Información general",
        "detalle": "Texas Heart Institute · s.f.",
        "url": "https://www.texasheart.org/heart-health/heart-information-center/topics/ataque-cardiaco/",
    },
    {
        "titulo": "Heart disease risk factors",
        "detalle": "National Heart, Lung, and Blood Institute · s.f.",
        "url": "https://www.nhlbi.nih.gov",
    },
    {
        "titulo": "Insuficiencia cardíaca",
        "detalle": "MSD Manuals · s.f.",
        "url": "https://www.msdmanuals.com/es/hogar/trastornos-del-corazón",
    },
    {
        "titulo": "Exploratory Data Analysis (EDA)",
        "detalle": "IBM Think / John W. Tukey · 1977-2024",
        "url": "https://www.ibm.com/mx-es/think/topics/exploratory-data-analysis",
    },
    {
        "titulo": "¿Qué es el algoritmo de k vecinos más cercanos (KNN)?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/mx-es/think/topics/knn",
    },
    {
        "titulo": "¿Qué es un Random Forest?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/mx-es/think/topics/random-forest",
    },
    {
        "titulo": "¿Qué es una Máquina de Vectores de Soporte (SVM)?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/es-es/think/topics/support-vector-machine",
    },
    {
        "titulo": "¿Qué es la Regresión Logística?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/es-es/think/topics/logistic-regression",
    },
    {
        "titulo": "¿Qué es XGBoost?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/es-es/think/topics/xgboost",
    },
    {
        "titulo": "Clasificación con datos desbalanceados",
        "detalle": "Aprende Machine Learning · s.f.",
        "url": "https://www.aprendemachinelearning.com/clasificacion-con-datos-desbalanceados/",
    },
    {
        "titulo": "Validación cruzada K-fold estratificada",
        "detalle": "GeeksforGeeks · 2025",
        "url": "https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/",
    },
    {
        "titulo": "¿Qué es un pipeline de machine learning?",
        "detalle": "IBM · s.f.",
        "url": "https://www.ibm.com/es-es/think/topics/machine-learning-pipeline",
    },
    {
        "titulo": "AUC y la curva ROC en aprendizaje automático",
        "detalle": "DataCamp · 2024",
        "url": "https://www.datacamp.com/tutorial/auc",
    },
    {
        "titulo": "Threshold tuning and monitoring",
        "detalle": "IBM · 2026",
        "url": "https://www.ibm.com/docs/en/omegamon-for-storage",
    },
    {
        "titulo": "SciPy: Open Source Scientific Tools for Python",
        "detalle": "Virtanen, P. et al. · Nature Methods · 2020",
        "url": "https://scipy.org/",
    },
    {
        "titulo": "Plotly Dash — Analytical Web Apps for Python",
        "detalle": "Plotly Technologies Inc. · 2024",
        "url": "https://dash.plotly.com/",
    },
    {
        "titulo": "Pandas — Python Data Analysis Library",
        "detalle": "The Pandas Development Team · 2024",
        "url": "https://pandas.pydata.org/",
    },
]
layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Referencias", style=TITLE_STYLE),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(f"{i+1}.", style={
                            "color": "#FBF7F7",
                            "fontWeight": "700",
                            "fontFamily": "'Poppins', sans-serif",
                            "fontSize": "0.9rem",
                            "flexShrink": "0",
                            "marginRight": "1rem",
                            "width": "24px"
                        }),
                        html.Div([
                            html.Span(ref["titulo"], style={
                                "color": "#ffffff",
                                "fontFamily": "'Poppins', sans-serif",
                                "fontWeight": "600",
                                "fontSize": "0.92rem",
                                "display": "block",
                                "marginBottom": "0.2rem"
                            }),
                            html.Span(ref["detalle"], style={
                                "color": "#94a3b8",
                                "fontFamily": "'Poppins', sans-serif",
                                "fontSize": "0.82rem",
                            }),
                        ], style={"flexGrow": "1"}),
                        html.A("→", href=ref["url"], target="_blank", style={
                            "color": "#C0392B",
                            "fontWeight": "700",
                            "fontSize": "1rem",
                            "textDecoration": "none",
                            "flexShrink": "0",
                            "marginLeft": "1rem"
                        })
                    ], style={
                        "display": "flex",
                        "alignItems": "center",
                        "padding": "1rem 1.2rem",
                        "backgroundColor": "#0D1B2E" if i % 2 == 0 else "#111827",
                        "borderBottom": "1px solid #1e3a5f",
                    })
                ])
                for i, ref in enumerate(referencias)
            ], style={
                "borderRadius": "12px",
                "overflow": "hidden",
                "border": "1px solid #1e3a5f"
            })
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})