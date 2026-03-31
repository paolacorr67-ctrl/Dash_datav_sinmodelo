import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
import os

dash.register_page(__name__, path="/sintesis", name="Síntesis")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "docs", "heart_disease_health_indicators_BRFSS2015.csv"))

TITLE_STYLE = {
    "color": "#ffffff", "fontWeight": "800", "fontSize": "1.6rem",
    "borderLeft": "6px solid #C0392B", "paddingLeft": "14px",
    "marginBottom": "0.5rem", "fontFamily": "'Poppins', sans-serif"
}
SUBTITLE_STYLE = {
    "color": "#94a3b8", "fontSize": "0.9rem",
    "fontFamily": "'Poppins', sans-serif", "marginBottom": "1rem"
}
TEXT_STYLE = {
    "color": "#cbd5e1", "fontSize": "0.92rem", "lineHeight": "1.8",
    "fontFamily": "'Poppins', sans-serif", "textAlign": "justify"
}
CARD_STYLE = {
    "backgroundColor": "#0D1B2E", "border": "1px solid #1e3a5f", "borderRadius": "12px"
}

target = "HeartDiseaseorAttack"
binary_vars = [
    "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
    "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump",
    "AnyHealthcare", "NoDocbcCost", "DiffWalk", "Sex"
]
ordinal_vars = ["GenHlth", "Age", "Education", "Income", "Diabetes"]
continuous_vars = ["BMI", "MentHlth", "PhysHlth"]
all_vars = binary_vars + ordinal_vars + continuous_vars

ranking = []
for var in all_vars:
    ct = pd.crosstab(df[var], df[target])
    chi2, pval, _, _ = chi2_contingency(ct)
    v = association(ct, method="cramer")
    ranking.append({"Variable": var, "V de Cramér": round(v, 4)})

ranking_df = pd.DataFrame(ranking).sort_values("V de Cramér", ascending=False).reset_index(drop=True)

hallazgos = [
    {
        "num": "01",
        "titulo": "Desbalance de clases crítico",
        "texto": "El 90.58% de los registros no presenta enfermedad cardíaca versus el 9.42% que sí. Este desbalance es un factor determinante para la futura modelación predictiva y requiere estrategias como SMOTE o ajuste de pesos de clase.",
        "color": "#C0392B"
    },
    {
        "num": "02",
        "titulo": "Salud general como predictor estrella",
        "texto": "GenHlth (autopercepción de salud) es la variable con mayor asociación con enfermedad cardíaca (V de Cramér más alto). A peor salud percibida, mayor prevalencia cardíaca, con una gradiente clara y consistente.",
        "color": "#C0392B"
    },
    {
        "num": "03",
        "titulo": "Edad y comorbilidades como factores clave",
        "texto": "La edad, la dificultad para caminar, el ACV previo y la diabetes muestran las asociaciones más fuertes junto con GenHlth. Los grupos de 65 años en adelante concentran la mayoría de los casos positivos.",
        "color": "#2C3E6B"
    },
    {
        "num": "04",
        "titulo": "Factores clínicos superan a los conductuales",
        "texto": "Variables clínicas como hipertensión, colesterol alto y diabetes tienen mayor poder predictivo que factores conductuales como el consumo de frutas, verduras o alcohol.",
        "color": "#2C3E6B"
    },
    {
        "num": "05",
        "titulo": "Dataset robusto y limpio",
        "texto": "El dataset no presenta valores nulos. Las 22 variables están dentro de sus rangos esperados. Los 23.899 duplicados se mantienen por ser estadísticamente plausibles en una encuesta poblacional con variables binarias.",
        "color": "#E8A838"
    },
    {
        "num": "06",
        "titulo": "Sesgo socioeconómico en la muestra",
        "texto": "La muestra está sobrerrepresentada por personas de alto nivel educativo e ingresos altos, sesgo típico de encuestas telefónicas. Este factor debe considerarse al generalizar los resultados.",
        "color": "#E8A838"
    },
]

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Síntesis General", style=TITLE_STYLE),
            html.P(
                "Principales hallazgos del análisis exploratorio del dataset BRFSS 2015.",
                style={**SUBTITLE_STYLE, "marginBottom": "0"}
            ),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    # Cards métricas globales
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("253.680", style={"color": "#F8F5F5", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("registros analizados", style={"textAlign": "center",
                "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("22", style={"color": "#FEFCFC", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("variables clasificadas", style={"textAlign": "center",
                "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3("9.42%", style={"color": "#FAF7F6", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
            html.P("prevalencia de enfermedad cardíaca", style={"textAlign": "center",
                "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(ranking_df.iloc[0]["Variable"], style={"color": "#F9F7F7", "fontWeight": "800",
                "textAlign": "center", "fontFamily": "'Poppins', sans-serif",
                "fontSize": "1.4rem"}),
            html.P("variable con mayor asociación", style={"textAlign": "center",
                "color": "#ffffff", "fontSize": "0.85rem", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=3, className="mb-4"),
    ]),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Hallazgos clave
    dbc.Row([
        dbc.Col([
            html.H4("Hallazgos Clave", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "0.4rem"
            }),
            html.P("Los principales patrones identificados en el análisis exploratorio.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.Div(style={
                        "width": "4px",
                        "backgroundColor": h["color"],
                        "borderRadius": "4px",
                        "flexShrink": "0",
                        "marginRight": "1rem",
                        "alignSelf": "stretch"
                    }),
                    html.Div([
                        html.Div([
                            html.Span(h["num"], style={
                                "color": h["color"],
                                "fontWeight": "800",
                                "fontSize": "1rem",
                                "fontFamily": "'Poppins', sans-serif",
                                "marginRight": "0.6rem"
                            }),
                            html.Span(h["titulo"], style={
                                "color": "#ffffff",
                                "fontWeight": "700",
                                "fontSize": "0.95rem",
                                "fontFamily": "'Poppins', sans-serif",
                            }),
                        ], style={"marginBottom": "0.5rem"}),
                        html.P(h["texto"], style={**TEXT_STYLE, "marginBottom": "0"})
                    ])
                ], style={
                    "display": "flex",
                    "padding": "1.2rem",
                    "backgroundColor": "#0D1B2E",
                    "border": "1px solid #1e3a5f",
                    "borderRadius": "12px",
                    "marginBottom": "0.8rem"
                })
            ])
            for h in hallazgos
        ])
    ], className="mb-5"),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # Conclusión ampliada
    dbc.Row([
        dbc.Col([
            html.H4("Conclusión", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "1rem"
            }),
            dbc.Card(dbc.CardBody([

                html.P(
                    "El análisis exploratorio del dataset BRFSS 2015 permitió caracterizar de forma "
                    "detallada el perfil de salud de 253.680 adultos estadounidenses y su relación "
                    "con la enfermedad cardíaca. A lo largo del análisis se aplicaron técnicas "
                    "descriptivas, pruebas estadísticas no paramétricas y medidas de asociación que "
                    "en conjunto ofrecen una visión comprehensiva de los factores de riesgo "
                    "cardiovascular presentes en la muestra.",
                    style={**TEXT_STYLE, "marginBottom": "1rem"}
                ),

                html.P(
                    "La autopercepción de salud general (GenHlth), la edad, la dificultad para "
                    "caminar y el antecedente de ACV emergen como los predictores más potentes, "
                    "seguidos por factores clínicos como la hipertensión, la diabetes y el colesterol "
                    "alto. Todos estos factores presentaron asociaciones estadísticamente significativas "
                    "con p-valores cercanos a cero, confirmando que su relación con la enfermedad "
                    "cardíaca no es producto del azar sino de patrones reales en la población.",
                    style={**TEXT_STYLE, "marginBottom": "1rem"}
                ),

                html.P(
                    "Un hallazgo relevante es que los factores clínicos y sociodemográficos superan "
                    "en poder predictivo a los conductuales. Variables como el consumo de frutas, "
                    "verduras o alcohol muestran asociaciones modestas en comparación con condiciones "
                    "crónicas preexistentes. Esto sugiere que la enfermedad cardíaca está más "
                    "fuertemente determinada por el estado de salud acumulado a lo largo de la vida "
                    "que por hábitos individuales aislados.",
                    style={**TEXT_STYLE, "marginBottom": "1rem"}
                ),

                html.P(
                    "El marcado desbalance de clases (90.58% vs 9.42%) representa el principal "
                    "desafío metodológico para la futura modelación predictiva. Se recomienda el uso "
                    "de técnicas de balanceo como SMOTE o undersampling, junto con métricas ajustadas "
                    "como F1-score, AUC-ROC y Recall para la clase positiva, evitando que el modelo "
                    "optimice únicamente la exactitud global a expensas de la detección de casos "
                    "reales de enfermedad cardíaca.",
                    style={**TEXT_STYLE, "marginBottom": "1rem"}
                ),

                html.P(
                    "Finalmente, es importante considerar el sesgo de selección inherente al BRFSS: "
                    "la muestra sobrerrepresenta personas de alto nivel educativo e ingresos altos, "
                    "lo que limita la generalización de los resultados a poblaciones de menor acceso "
                    "socioeconómico. A pesar de esto, el dataset constituye una base sólida y bien "
                    "documentada para el desarrollo de modelos de clasificación de riesgo "
                    "cardiovascular.",
                    style={**TEXT_STYLE, "marginBottom": "0"}
                ),

            ]), style={**CARD_STYLE, "borderLeft": "5px solid #C0392B"})
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})