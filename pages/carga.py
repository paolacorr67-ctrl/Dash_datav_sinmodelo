import dash
from dash import html, dash_table, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os

dash.register_page(__name__, path="/carga", name="Carga")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "docs", "heart_disease_health_indicators_BRFSS2015.csv"))

TITLE_STYLE = {
    "color": "#ffffff", "fontWeight": "800", "fontSize": "1.6rem",
    "borderLeft": "6px solid #C0392B", "paddingLeft": "14px",
    "marginBottom": "0.5rem", "fontFamily": "'Poppins', sans-serif"
}
SUBTITLE_STYLE = {
    "color": "#94a3b8", "fontSize": "0.9rem",
    "fontFamily": "'Poppins', sans-serif", "marginBottom": "1.5rem"
}
TEXT_STYLE = {
    "color": "#cbd5e1", "fontSize": "0.92rem", "lineHeight": "1.8",
    "fontFamily": "'Poppins', sans-serif", "textAlign": "justify",
}
TABLE_HEADER = {
    "backgroundColor": "#162032", "color": "#ffffff", "fontWeight": "600",
    "border": "1px solid #1e3a5f", "fontFamily": "'Poppins', sans-serif", "fontSize": "0.85rem"
}
TABLE_CELL = {
    "backgroundColor": "#0D1B2E", "color": "#cbd5e1", "border": "1px solid #1e3a5f",
    "padding": "10px 14px", "fontFamily": "'Poppins', sans-serif", "fontSize": "0.85rem"
}

DD_STYLE = {
    "backgroundColor": "#0D1B2E", 
    "border": "1px solid #1e3a5f", "borderRadius": "8px",
    "fontFamily": "'Poppins', sans-serif", "fontSize": "0.88rem"
}

diccionario = [
    {"Variable": "HeartDiseaseorAttack", "Tipo": "Objetivo",  "Escala": "0 / 1",       "Descripción": "Reportó enfermedad coronaria o infarto"},
    {"Variable": "HighBP",               "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Diagnóstico de presión arterial alta"},
    {"Variable": "HighChol",             "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Diagnóstico de colesterol alto"},
    {"Variable": "CholCheck",            "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Revisión de colesterol en últimos 5 años"},
    {"Variable": "BMI",                  "Tipo": "Continua",  "Escala": "12 – 98",     "Descripción": "Índice de masa corporal"},
    {"Variable": "Smoker",               "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Fumó al menos 100 cigarrillos en su vida"},
    {"Variable": "Stroke",               "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Diagnóstico de derrame cerebral (ACV)"},
    {"Variable": "Diabetes",             "Tipo": "Ordinal",   "Escala": "0 / 1 / 2",   "Descripción": "0=Sin diabetes · 1=Prediabetes · 2=Diabetes confirmada"},
    {"Variable": "PhysActivity",         "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Realizó actividad física en últimos 30 días"},
    {"Variable": "Fruits",               "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Consume frutas 1 o más veces al día"},
    {"Variable": "Veggies",              "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Consume verduras 1 o más veces al día"},
    {"Variable": "HvyAlcoholConsump",    "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Consumo excesivo de alcohol"},
    {"Variable": "AnyHealthcare",        "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Tiene cobertura o seguro médico"},
    {"Variable": "NoDocbcCost",          "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "No fue al médico en el último año por costo"},
    {"Variable": "GenHlth",              "Tipo": "Ordinal",   "Escala": "1 – 5",       "Descripción": "Autopercepción de salud general (1=Excelente · 5=Mala)"},
    {"Variable": "MentHlth",             "Tipo": "Continua",  "Escala": "0 – 30 días", "Descripción": "Días con mala salud mental en el último mes"},
    {"Variable": "PhysHlth",             "Tipo": "Continua",  "Escala": "0 – 30 días", "Descripción": "Días con mala salud física en el último mes"},
    {"Variable": "DiffWalk",             "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "Dificultad seria para caminar o subir escaleras"},
    {"Variable": "Sex",                  "Tipo": "Binaria",   "Escala": "0 / 1",       "Descripción": "0 = Mujer · 1 = Hombre"},
    {"Variable": "Age",                  "Tipo": "Ordinal",   "Escala": "1 – 13",      "Descripción": "Grupo etario en intervalos de 5 años (1=18–24 · 13=80+)"},
    {"Variable": "Education",            "Tipo": "Ordinal",   "Escala": "1 – 6",       "Descripción": "Nivel educativo (1=Sin escolaridad · 6=Universitario)"},
    {"Variable": "Income",               "Tipo": "Ordinal",   "Escala": "1 – 8",       "Descripción": "Ingreso anual del hogar (1=<$10k · 8=≥$75k)"},
]

tipos = ["Todos", "Objetivo", "Binaria", "Ordinal", "Continua"]

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Carga y Estructura del Dataset", style=TITLE_STYLE),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(f"{df.shape[0]:,}", style={"color": "#C0392B", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("filas", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style={"backgroundColor": "#0D1B2E", "border": "1px solid #1e3a5f",
            "borderRadius": "10px"}), md=4, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(f"{df.shape[1]}", style={"color": "#C0392B", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("columnas", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style={"backgroundColor": "#0D1B2E", "border": "1px solid #1e3a5f",
            "borderRadius": "10px"}), md=4, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("float64", style={"color": "#C0392B", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("tipo de dato original", style={"textAlign": "center", "color": "#ffffff",
                "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style={"backgroundColor": "#0D1B2E", "border": "1px solid #1e3a5f",
            "borderRadius": "10px"}), md=4, className="mb-4"),
    ]),

    dbc.Row([
        dbc.Col([
            html.P("El dataset cargado contiene 253.680 registros y 22 variables, resultado "
                "del proceso de limpieza y selección aplicado sobre el BRFSS 2015 original "
                "de 441.456 filas y 330 columnas. De las 22 variables, 1 corresponde a la "
                "variable objetivo (HeartDiseaseorAttack) y las 21 restantes representan "
                "los factores de riesgo seleccionados.", style=TEXT_STYLE),
            html.P("El hecho de que todas sean float64 es solo el formato de almacenamiento, "
                "no su naturaleza estadística. Clasificarlas correctamente es importante "
                "porque determina qué tipo de visualizaciones y estadísticas aplicar en el EDA.",
                style=TEXT_STYLE),
        ])
    ], className="mb-4"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    dbc.Row([
        dbc.Col([
            html.H4("Vista previa del dataset", style={"color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif", "fontWeight": "700", "marginBottom": "1rem"}),
            html.P("¿Cuántas filas quieres explorar?", style={"color": "#94a3b8",
                "fontSize": "0.85rem", "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.8rem"}),
            dcc.Slider(id="slider-filas", min=5, max=20, step=5, value=10,
                marks={i: {"label": str(i), "style": {"color": "#94a3b8"}} for i in [5, 10, 15, 20]},
                tooltip={"placement": "bottom", "always_visible": False}),
            html.Div(id="tabla-preview", style={"marginTop": "1.5rem"}),
        ])
    ], className="mb-5"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    dbc.Row([
        dbc.Col([
            html.H4("Diccionario de variables", style={"color": "#ffffff",
                "fontFamily": "'Poppins', sans-serif", "fontWeight": "700", "marginBottom": "1rem"}),
            dbc.Row([
                dbc.Col([
                    html.Label("Filtrar por tipo:", style={"color": "#94a3b8", "fontSize": "0.85rem",
                        "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.3rem"}),
                    dcc.Dropdown(
                        id="dropdown-tipo",
                        options=[{"label": t, "value": t} for t in tipos],
                        value="Objetivo",
                        clearable=False,
                        className="dark-dropdown",
                        style=DD_STYLE
                    ),
                ], md=4),
                dbc.Col([
                    html.Div(id="contador-variables", style={"color": "#929caa",
                        "fontSize": "0.85rem", "fontFamily": "'Poppins', sans-serif", "marginTop": "2rem"})
                ], md=4),
            ], className="mb-3"),
            html.Div(id="tabla-diccionario"),
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


@callback(Output("tabla-preview", "children"), Input("slider-filas", "value"))
def update_preview(n_filas):
    preview = df.head(n_filas).round(2)
    return dash_table.DataTable(
        data=preview.to_dict("records"),
        columns=[{"name": c, "id": c} for c in preview.columns],
        style_table={"overflowX": "auto", "borderRadius": "10px"},
        style_header=TABLE_HEADER, style_cell=TABLE_CELL,
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#111827"}],
        page_size=n_filas,
    )


@callback(Output("tabla-diccionario", "children"), Output("contador-variables", "children"),
          Input("dropdown-tipo", "value"))
def update_diccionario(tipo):
    data = diccionario if tipo == "Todos" else [d for d in diccionario if d["Tipo"] == tipo]
    tabla = dash_table.DataTable(
        data=data,
        columns=[{"name": "Variable", "id": "Variable"}, {"name": "Tipo", "id": "Tipo"},
                 {"name": "Escala", "id": "Escala"}, {"name": "Descripción", "id": "Descripción"}],
        style_table={"overflowX": "auto", "borderRadius": "10px"},
        style_header=TABLE_HEADER,
        style_cell={**TABLE_CELL, "whiteSpace": "normal", "height": "auto"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#111827"},
            {"if": {"filter_query": '{Tipo} = "Objetivo"'}, "backgroundColor": "#1a2a4a", "color": "#ffffff"},
        ],
        page_size=22,
    )
    contador = f"Mostrando {len(data)} variable{'s' if len(data) != 1 else ''}"
    return tabla, contador