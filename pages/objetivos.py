import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/objetivos", name="Objetivos")

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

especificos = [
    {
        "id": "obj1",
        "num": "01",
        "titulo": "Distribución de variables",
        "detalle": (
            "Describir la distribución de las variables clínicas, conductuales y "
            "sociodemográficas presentes en el dataset BRFSS 2015, identificando "
            "frecuencias, proporciones y posibles valores atípicos. Este objetivo "
            "sienta las bases para entender el comportamiento individual de cada "
            "variable antes de explorar sus relaciones."
        ),
    },
    {
        "id": "obj2",
        "num": "02",
        "titulo": "Desbalance de clases",
        "detalle": (
            "Analizar el desbalance de clases en la variable objetivo "
            "(HeartDiseaseorAttack) y evaluar su implicación para el análisis "
            "y la futura modelación. Con solo un 9.42% de casos positivos, "
            "este desbalance es crítico para decisiones de modelado como el "
            "uso de SMOTE o ajuste de pesos de clase."
        ),
    },
    {
        "id": "obj3",
        "num": "03",
        "titulo": "Factores de riesgo cardiovascular",
        "detalle": (
            "Examinar la relación entre los factores de riesgo cardiovascular "
            "—como hipertensión, colesterol elevado, tabaquismo, diabetes e "
            "índice de masa corporal— y la presencia de enfermedad cardíaca. "
            "Se aplican pruebas estadísticas como Chi² y V de Cramér para "
            "cuantificar la fuerza de cada asociación."
        ),
    },
    {
        "id": "obj4",
        "num": "04",
        "titulo": "Comparación entre grupos",
        "detalle": (
            "Comparar el perfil de salud y los hábitos de vida entre individuos "
            "con y sin enfermedad cardíaca, identificando contrastes "
            "estadísticamente relevantes. Se utilizan pruebas Mann-Whitney U "
            "para variables continuas y tasas de incidencia por grupo para "
            "una interpretación clínica directa."
        ),
    },
]


def make_card(obj):
    return dbc.Col([
        # Parte fija — siempre visible, mismo tamaño en todas
        html.Div([
            html.Div([
                html.Span(obj["num"], style={
                    "color": "#ffffff",
                    "fontWeight": "800",
                    "fontSize": "1.4rem",
                    "fontFamily": "'Poppins', sans-serif",
                    "flexShrink": "0"
                }),
                html.H6(obj["titulo"], style={
                    "color": "#ffffff",
                    "fontFamily": "'Poppins', sans-serif",
                    "fontWeight": "700",
                    "fontSize": "1rem",
                    "marginBottom": "0"
                }),
            ], style={
                "display": "flex",
                "alignItems": "center",
                "gap": "0.8rem",
                "marginBottom": "1.5rem"
            }),

            dbc.Button(
                "Ver más ↓",
                id=f"btn-{obj['id']}",
                size="sm",
                style={
                    "fontFamily": "'Poppins', sans-serif",
                    "fontSize": "0.8rem",
                    "backgroundColor": "transparent",
                    "border": "1px solid #ffffff",
                    "color": "#ffffff",
                    "borderRadius": "6px",
                    "padding": "0.3rem 0.8rem"
                }
            ),
        ], style={
            "backgroundColor": "#0D1B2E",
            "border": "1px solid #1e3a5f",
            "borderRadius": "12px",
            "padding": "1.2rem",
            "height": "140px",              # altura fija igual en todas
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "space-between"
        }),

        # Parte colapsable — crece hacia abajo
        dbc.Collapse(
            html.Div([
                html.P(obj["detalle"], style={**TEXT_STYLE, "marginBottom": "0"})
            ], style={
                "backgroundColor": "#162032",
                "borderLeft": "4px solid #C0392B",
                "borderRadius": "0 0 12px 12px",
                "padding": "1rem 1.2rem",
                "marginTop": "2px"
            }),
            id=f"collapse-{obj['id']}",
            is_open=False
        )
    ], md=6, className="mb-4")


layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Objetivos", style=TITLE_STYLE),
            html.P(
                "Propósitos que guían el análisis exploratorio del dataset BRFSS 2015.",
                style={**SUBTITLE_STYLE, "marginBottom": "0"}
            ),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    dbc.Row([
        dbc.Col([
            html.H4("Objetivo General", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "1rem"
            }),
            dbc.Card(dbc.CardBody([
                html.P(
                    "Examinar, a través de técnicas de análisis exploratorio y visualización "
                    "de datos, qué factores conductuales, clínicos y sociodemográficos "
                    "presentan mayor asociación con el riesgo de enfermedad cardíaca en "
                    "adultos estadounidenses, detectando patrones, contrastes entre grupos "
                    "y variables con mayor capacidad explicativa como base para una futura "
                    "modelación predictiva.",
                    style={**TEXT_STYLE, "marginBottom": "0"}
                )
            ]), style={
                "backgroundColor": "#0D1B2E",
                "borderRadius": "12px",
                "borderLeft": "5px solid #C0392B",
                "border": "1px solid #1e3a5f"
            })
        ])
    ], className="mb-5"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    dbc.Row([
        dbc.Col([
            html.H4("Objetivos Específicos", style={
                "color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700",
                "marginBottom": "0.4rem"
            }),
            html.P("Haz click en cada card para expandir los detalles.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"})
        ])
    ]),

    dbc.Row([make_card(obj) for obj in especificos]),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


for obj in especificos:
    @callback(
        Output(f"collapse-{obj['id']}", "is_open"),
        Output(f"btn-{obj['id']}", "children"),
        Input(f"btn-{obj['id']}", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_collapse(n, obj_id=obj["id"]):
        is_open = n % 2 != 0
        label = "Ver menos ↑" if is_open else "Ver más ↓"
        return is_open, label