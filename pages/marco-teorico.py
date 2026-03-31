import dash
from dash import html, Input, Output, callback, ALL, ctx
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path="/marco-teorico", name="Marco Teórico")

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
    "textAlign": "justify",
    "marginBottom": "0"
}

temas = [
    {
        "id": "tema1",
        "titulo": "Enfermedades cardíacas e insuficiencia cardíaca",
        "contenido": (
            "La insuficiencia cardíaca es un trastorno en el que el corazón es incapaz de "
            "satisfacer las demandas del organismo, lo que genera una reducción del flujo "
            "sanguíneo y congestión en venas y pulmones. Puede originarse por causas directas "
            "—como el debilitamiento o rigidez del músculo cardíaco— o indirectas, producto de "
            "condiciones como la hipertensión arterial, la diabetes o valvulopatías. En muchos "
            "casos, los síntomas como la disnea y el cansancio se desarrollan gradualmente, lo "
            "que dificulta su detección temprana y refuerza la importancia de la vigilancia "
            "poblacional continua."
        )
    },
    {
        "id": "tema2",
        "titulo": "El sistema BRFSS como fuente de datos",
        "contenido": (
            "El Sistema de Vigilancia de Factores de Riesgo Conductuales (BRFSS) es el principal "
            "sistema nacional de encuestas telefónicas sobre salud en Estados Unidos, administrado "
            "por los CDC desde 1984. Recopila datos en los 50 estados, el Distrito de Columbia y "
            "territorios participantes, con más de 400.000 entrevistas a adultos cada año, siendo "
            "el sistema de encuestas telefónicas de salud continua más grande del mundo. Su objetivo "
            "es monitorear conductas de riesgo, enfermedades crónicas, acceso a atención médica y "
            "uso de servicios preventivos, convirtiéndose en una herramienta clave para la "
            "planificación de políticas de salud pública a nivel estatal y local."
        )
    },
    {
        "id": "tema3",
        "titulo": "Análisis Exploratorio de Datos (EDA)",
        "contenido": (
            "El análisis exploratorio de datos (EDA, por sus siglas en inglés) es un enfoque "
            "metodológico que permite examinar conjuntos de datos para resumir sus características "
            "principales, descubrir patrones, detectar anomalías y evaluar supuestos antes de "
            "aplicar técnicas de modelado formal. Desarrollado por el matemático John Tukey en la "
            "década de 1970, el EDA emplea principalmente métodos de visualización estadística para "
            "revelar relaciones entre variables y orientar decisiones sobre el análisis posterior. "
            "En el contexto de datos de salud, resulta especialmente valioso para identificar "
            "factores de riesgo relevantes y comprender la estructura del problema antes de "
            "construir modelos predictivos."
        )
    },
]

metricas = [
    {
        "id": "met1",
        "nombre": "Chi-cuadrado (χ²)",
        "resumen": "Asociación entre variables categóricas.",
        "descripcion": (
            "Prueba de hipótesis que evalúa si existe una asociación estadísticamente "
            "significativa entre dos variables categóricas. Compara las frecuencias observadas "
            "en una tabla de contingencia contra las que se esperarían si las variables fueran "
            "independientes."
        ),
        "uso": "Determinar si cada variable binaria u ordinal tiene relación no aleatoria con HeartDiseaseorAttack."
    },
    {
        "id": "met2",
        "nombre": "V de Cramér",
        "resumen": "Magnitud de la asociación entre variables.",
        "descripcion": (
            "Medida de efecto derivada del estadístico Chi-cuadrado, normalizada en un rango "
            "de 0 a 1, donde 0 indica ausencia total de asociación y 1 asociación perfecta. "
            "Permite comparar la fuerza de asociación entre variables con diferente número de categorías."
        ),
        "uso": "Cuantificar la magnitud de la asociación más allá de la significancia estadística."
    },
    {
        "id": "met3",
        "nombre": "Mann-Whitney U",
        "resumen": "Comparación de distribuciones sin asumir normalidad.",
        "descripcion": (
            "Prueba no paramétrica que compara las distribuciones de una variable continua "
            "entre dos grupos independientes, sin asumir normalidad. Más robusta que la "
            "t de Student cuando los datos presentan sesgo pronunciado."
        ),
        "uso": "Comparar BMI, MentHlth y PhysHlth entre grupos con y sin enfermedad cardíaca."
    },
    {
        "id": "met4",
        "nombre": "Correlación de Pearson (r)",
        "resumen": "Fuerza y dirección de relación lineal entre variables.",
        "descripcion": (
            "Mide la fuerza y dirección de la relación lineal entre dos variables numéricas, "
            "en un rango de −1 a 1. Permite identificar de forma rápida qué predictores se "
            "relacionan positiva o negativamente con el riesgo cardíaco."
        ),
        "uso": "Síntesis visual de la fuerza lineal de asociación de todas las variables con el target."
    },
]


def make_collapsible(item, prefix):
    return html.Div([
        html.Div([
            html.Span(item["titulo"] if "titulo" in item else item["nombre"], style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "600",
                "fontSize": "0.95rem",
                "flexGrow": "1"
            }),
            html.Span("▼", id={"type": f"arrow-{prefix}", "index": item["id"]}, style={
                "color": "#94a3b8",
                "fontSize": "0.8rem"
            }),
        ],
        id={"type": f"header-{prefix}", "index": item["id"]},
        n_clicks=0,
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "0.8rem",
            "padding": "1rem 1.2rem",
            "backgroundColor": "#0D1B2E",
            "border": "1px solid #1e3a5f",
            "borderRadius": "10px",
            "cursor": "pointer",
            "marginBottom": "0.5rem"
        }),

        dbc.Collapse(
            html.Div([
                html.P(item["contenido"] if "contenido" in item else item["descripcion"],
                    style=TEXT_STYLE),
                html.Div([
                    html.Span("Uso: ", style={
                        "color": "#ffffff",
                        "fontWeight": "600",
                        "fontSize": "0.85rem",
                        "fontFamily": "'Poppins', sans-serif"
                    }),
                    html.Span(item.get("uso", ""), style={
                        "color": "#94a3b8",
                        "fontSize": "0.85rem",
                        "fontFamily": "'Poppins', sans-serif"
                    }),
                ], style={"marginTop": "0.8rem"} if "uso" in item else {"display": "none"})
            ], style={
                "padding": "1rem 1.2rem",
                "backgroundColor": "#162032",
                "borderLeft": "4px solid #C0392B",
                "borderRadius": "0 0 10px 10px",
                "marginTop": "-0.5rem",
                "marginBottom": "0.5rem"
            }),
            id={"type": f"collapse-{prefix}", "index": item["id"]},
            is_open=False
        )
    ])


layout = dbc.Container([

    # Título
    dbc.Row([
        dbc.Col([
            html.H1("Marco Teórico", style=TITLE_STYLE),
            html.P(
                "Fundamentos conceptuales y estadísticos que sustentan el análisis.",
                style=SUBTITLE_STYLE
            ),
            html.Hr(style={"borderColor": "#1e3a5f"}),
        ])
    ], className="mt-4"),

    # Conceptos fundamentales
    dbc.Row([
        dbc.Col([
            html.H4("Conceptos Fundamentales", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "0.4rem"
            }),
            html.P("Haz click en cada tema para expandirlo.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.2rem"}),
            html.Div([make_collapsible(t, "tema") for t in temas]),
        ])
    ], className="mb-4"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Métricas estadísticas
    dbc.Row([
        dbc.Col([
            html.H4("Métricas Estadísticas", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "0.4rem"
            }),
            html.P("Herramientas estadísticas aplicadas en el análisis bivariado.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.2rem"}),
            html.Div([make_collapsible(m, "met") for m in metricas]),
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


# Callback temas — cuando uno abre, los demás se cierran
@callback(
    Output({"type": "collapse-tema", "index": ALL}, "is_open"),
    Output({"type": "arrow-tema", "index": ALL}, "children"),
    Input({"type": "header-tema", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def toggle_temas(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        return [False] * len(temas), ["▼"] * len(temas)

    ids = [t["id"] for t in temas]
    clicked = triggered["index"]

    is_open_list = []
    arrow_list = []
    for tid in ids:
        if tid == clicked:
            idx = ids.index(tid)
            currently_open = n_clicks[idx] % 2 != 0
            is_open_list.append(currently_open)
            arrow_list.append("▲" if currently_open else "▼")
        else:
            is_open_list.append(False)
            arrow_list.append("▼")

    return is_open_list, arrow_list


# Callback métricas — cuando una abre, las demás se cierran
@callback(
    Output({"type": "collapse-met", "index": ALL}, "is_open"),
    Output({"type": "arrow-met", "index": ALL}, "children"),
    Input({"type": "header-met", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def toggle_metricas(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        return [False] * len(metricas), ["▼"] * len(metricas)

    ids = [m["id"] for m in metricas]
    clicked = triggered["index"]

    is_open_list = []
    arrow_list = []
    for mid in ids:
        if mid == clicked:
            idx = ids.index(mid)
            currently_open = n_clicks[idx] % 2 != 0
            is_open_list.append(currently_open)
            arrow_list.append("▲" if currently_open else "▼")
        else:
            is_open_list.append(False)
            arrow_list.append("▼")

    return is_open_list, arrow_list