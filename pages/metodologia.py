import dash
from dash import html, Input, Output, callback, ALL, ctx
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/metodologia", name="Metodología")

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

univariado = [
    {
        "id": "uni1",
        "titulo": "Variables binarias",
        "descripcion": (
            "Se calcularán frecuencias absolutas y relativas con value_counts(), "
            "visualizadas en gráficos de barras verticales con el porcentaje anotado "
            "sobre cada barra. Cada gráfico es seguido de una interpretación narrativa "
            "con énfasis clínico."
        ),
        "uso": "Aplicado a variables como HighBP, HighChol, Smoker, Stroke, Sex, entre otras."
    },
    {
        "id": "uni2",
        "titulo": "Variables ordinales",
        "descripcion": (
            "Mismo cálculo de frecuencias, pero representadas con barras horizontales "
            "para acomodar las etiquetas. Se preserva el orden natural de las categorías "
            "y se usan paletas diferenciadas por nivel para reforzar el carácter ordinal "
            "de la escala."
        ),
        "uso": "Aplicado a variables como GenHlth, Age, Education, Income y Diabetes."
    },
    {
        "id": "uni3",
        "titulo": "Variables continuas",
        "descripcion": (
            "Se construye una tabla descriptiva con media, mediana, desviación estándar, "
            "cuartiles, IQR y conteo de outliers por criterio de Tukey. La visualización "
            "varía según la variable: BMI se grafica con histograma de 50 bins con líneas "
            "de media y mediana superpuestas; MentHlth y PhysHlth, al tomar valores enteros "
            "de 0 a 30, se representan con barras por valor exacto para identificar picos "
            "y concentración en el cero."
        ),
        "uso": "Aplicado a BMI, MentHlth y PhysHlth."
    },
]

bivariado = [
    {
        "id": "biv1",
        "titulo": "Variables binarias y ordinales → Chi-cuadrado + V de Cramér",
        "descripcion": (
            "La prueba χ² evalúa si existe asociación estadísticamente significativa entre "
            "cada variable predictora y la variable objetivo HeartDiseaseorAttack. "
            "La V de Cramér cuantifica la magnitud de dicha asociación en un rango [0, 1], "
            "permitiendo comparar la fuerza de asociación entre variables con diferente "
            "número de categorías."
        ),
        "uso": "Aplicado a las 13 variables binarias y las 5 variables ordinales del dataset."
    },
    {
        "id": "biv2",
        "titulo": "Variables continuas → Mann-Whitney U",
        "descripcion": (
            "Dado el sesgo pronunciado de BMI, MentHlth y PhysHlth, la prueba no paramétrica "
            "de Mann-Whitney es más robusta que la t de Student para comparar las distribuciones "
            "entre los dos grupos de la variable objetivo. No asume normalidad en los datos."
        ),
        "uso": "Aplicado a BMI, MentHlth y PhysHlth comparando grupos con y sin enfermedad cardíaca."
    },
    {
        "id": "biv3",
        "titulo": "Tasas de incidencia por grupo",
        "descripcion": (
            "Se calcula el porcentaje de personas con enfermedad cardíaca dentro de cada "
            "categoría de cada variable predictora. Este enfoque ofrece una interpretación "
            "clínica directa y permite identificar qué categorías concentran mayor riesgo "
            "cardiovascular."
        ),
        "uso": "Complementa los resultados estadísticos con una lectura clínica intuitiva."
    },
    {
        "id": "biv4",
        "titulo": "Mapa de calor de correlaciones de Pearson",
        "descripcion": (
            "Como síntesis visual, se construye un mapa de calor con la correlación de Pearson "
            "entre todas las variables del dataset y la variable objetivo. Permite identificar "
            "de forma rápida qué predictores se relacionan positiva o negativamente con el "
            "riesgo cardíaco y detectar posibles relaciones de colinealidad entre variables."
        ),
        "uso": "Síntesis global de asociaciones lineales entre todas las variables y el target."
    },
]


def make_collapsible(item, prefix):
    return html.Div([
        html.Div([
            html.Span(item["titulo"], style={
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
                html.P(item["descripcion"], style=TEXT_STYLE),
                html.Div([
                    html.Span("Aplicación: ", style={
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
                ], style={"marginTop": "0.8rem"})
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
            html.H1("Metodología", style=TITLE_STYLE),
            html.P(
                "Estrategias y técnicas aplicadas en el análisis univariado y bivariado.",
                style=SUBTITLE_STYLE
            ),
            html.Hr(style={"borderColor": "#1e3a5f"}),
        ])
    ], className="mt-4"),

    # Análisis univariado
    dbc.Row([
        dbc.Col([
            html.H4("Metodología del Análisis Univariado", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "0.4rem"
            }),
            html.P(
                "El análisis univariado se realizará según la naturaleza estadística de cada "
                "variable, aplicando técnicas descriptivas diferenciadas para tres grupos. "
                "Haz click en cada uno para ver el detalle.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.2rem"}
            ),
            html.Div([make_collapsible(u, "uni") for u in univariado]),
        ])
    ], className="mb-4"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Análisis bivariado
    dbc.Row([
        dbc.Col([
            html.H4("Metodología del Análisis Bivariado", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "0.4rem"
            }),
            html.P(
                "Para examinar la relación entre cada variable predictora y la variable objetivo, "
                "se emplean cuatro estrategias según el tipo estadístico de la variable. "
                "Haz click en cada una para ver el detalle.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.2rem"}
            ),
            html.Div([make_collapsible(b, "biv") for b in bivariado]),
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


# Callback univariado
@callback(
    Output({"type": "collapse-uni", "index": ALL}, "is_open"),
    Output({"type": "arrow-uni", "index": ALL}, "children"),
    Input({"type": "header-uni", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def toggle_univariado(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        return [False] * len(univariado), ["▼"] * len(univariado)

    ids = [u["id"] for u in univariado]
    clicked = triggered["index"]

    is_open_list, arrow_list = [], []
    for uid in ids:
        if uid == clicked:
            idx = ids.index(uid)
            currently_open = n_clicks[idx] % 2 != 0
            is_open_list.append(currently_open)
            arrow_list.append("▲" if currently_open else "▼")
        else:
            is_open_list.append(False)
            arrow_list.append("▼")

    return is_open_list, arrow_list


# Callback bivariado
@callback(
    Output({"type": "collapse-biv", "index": ALL}, "is_open"),
    Output({"type": "arrow-biv", "index": ALL}, "children"),
    Input({"type": "header-biv", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def toggle_bivariado(n_clicks):
    triggered = ctx.triggered_id
    if not triggered:
        return [False] * len(bivariado), ["▼"] * len(bivariado)

    ids = [b["id"] for b in bivariado]
    clicked = triggered["index"]

    is_open_list, arrow_list = [], []
    for bid in ids:
        if bid == clicked:
            idx = ids.index(bid)
            currently_open = n_clicks[idx] % 2 != 0
            is_open_list.append(currently_open)
            arrow_list.append("▲" if currently_open else "▼")
        else:
            is_open_list.append(False)
            arrow_list.append("▼")

    return is_open_list, arrow_list