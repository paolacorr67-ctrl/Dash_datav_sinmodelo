import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import chi2_contingency, mannwhitneyu
from scipy.stats.contingency import association
import os

dash.register_page(__name__, path="/resultados", name="Resultados")

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
PLOT_BASE = dict(
    paper_bgcolor="#0D1B2E", plot_bgcolor="#0D1B2E",
    font=dict(color="#cbd5e1", family="Poppins", size=12),
    margin=dict(t=50, b=50, l=50, r=30),
)
DROPDOWN_STYLE = {
    "backgroundColor": "#0D1B2E", "color": "#ffffff",
    "border": "1px solid #1e3a5f", "borderRadius": "8px",
    "fontFamily": "'Poppins', sans-serif", "fontSize": "0.88rem"
}

binary_vars = [
    "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
    "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump",
    "AnyHealthcare", "NoDocbcCost", "DiffWalk", "Sex"
]
ordinal_vars = ["GenHlth", "Age", "Education", "Income", "Diabetes"]
continuous_vars = ["BMI", "MentHlth", "PhysHlth"]
target_var = "HeartDiseaseorAttack"
all_vars = binary_vars + ordinal_vars + continuous_vars

mappings = {
    "HeartDiseaseorAttack": {0: "Sin enfermedad", 1: "Con enfermedad"},
    "HighBP":            {0: "Sin hipertensión",          1: "Con hipertensión"},
    "HighChol":          {0: "Sin colesterol alto",        1: "Con colesterol alto"},
    "CholCheck":         {0: "Sin chequeo",                1: "Con chequeo"},
    "Smoker":            {0: "No fumador",                 1: "Fumador"},
    "Stroke":            {0: "Sin ACV",                    1: "Con ACV"},
    "PhysActivity":      {0: "Sin actividad física",       1: "Con actividad física"},
    "Fruits":            {0: "No consume frutas",          1: "Consume frutas"},
    "Veggies":           {0: "No consume verduras",        1: "Consume verduras"},
    "HvyAlcoholConsump": {0: "No consumo alto",            1: "Consumo alto alcohol"},
    "AnyHealthcare":     {0: "Sin cobertura",              1: "Con cobertura médica"},
    "NoDocbcCost":       {0: "Sin barrera económica",      1: "Con barrera económica"},
    "DiffWalk":          {0: "Sin dificultad",             1: "Con dificultad al caminar"},
    "Sex":               {0: "Mujer",                      1: "Hombre"},
    "Diabetes":          {0: "Sin diabetes", 1: "Prediabetes", 2: "Diabetes confirmada"},
    "GenHlth":           {1: "Excelente", 2: "Muy buena", 3: "Buena", 4: "Regular", 5: "Mala"},
    "Age": {1:"18–24",2:"25–29",3:"30–34",4:"35–39",5:"40–44",6:"45–49",
            7:"50–54",8:"55–59",9:"60–64",10:"65–69",11:"70–74",12:"75–79",13:"80+"},
    "Education": {1:"Nunca asistió",2:"Primaria incompleta",3:"Secundaria incompleta",
                  4:"Secundaria completa",5:"Universidad incompleta",6:"Universidad completa"},
    "Income": {1:"< $10k",2:"$10–15k",3:"$15–20k",4:"$20–25k",
               5:"$25–35k",6:"$35–50k",7:"$50–75k",8:"$75k+"},
}

interp_uni = {
    "HighBP": "El 42.9% de los encuestados presenta hipertensión. Esta distribución es notable ya que casi la mitad de la muestra convive con presión arterial alta, uno de los principales factores de riesgo cardiovascular.",
    "HighChol": "El 42.41% presenta colesterol alto. La distribución es muy similar a HighBP, reflejando que cerca de cuatro de cada diez participantes tienen este factor de riesgo.",
    "CholCheck": "El 96.27% se realizó un chequeo de colesterol en los últimos 5 años, reflejando un alto nivel de adherencia a servicios preventivos de salud en la muestra.",
    "Smoker": "El 44.32% ha fumado al menos 100 cigarrillos en su vida. La distribución es relativamente equilibrada, siendo el tabaquismo uno de los tres factores de riesgo clave identificados por los CDC.",
    "Stroke": "Solo el 4.06% reportó haber sufrido un derrame cerebral. Aunque su baja prevalencia podría limitar su variabilidad, el ACV y la enfermedad cardíaca comparten múltiples factores de riesgo.",
    "PhysActivity": "El 75.65% realizó actividad física en los últimos 30 días. El cuarto de la población que no realiza ninguna actividad representa un grupo de interés dado que el sedentarismo es un factor de riesgo cardiovascular relevante.",
    "Fruits": "El 63.43% consume frutas al menos una vez al día. Más de un tercio no alcanza este mínimo dietético recomendado, lo que podría estar relacionado con mayor riesgo cardiovascular.",
    "Veggies": "El 81.14% consume verduras diariamente. Comparado con el consumo de frutas (63.43%), el hábito de consumir verduras está más extendido en la muestra.",
    "HvyAlcoholConsump": "Solo el 5.62% presenta consumo excesivo de alcohol. La distribución es muy asimétrica con gran concentración en la clase negativa.",
    "AnyHealthcare": "El 95.11% cuenta con cobertura médica, reflejando un alto nivel de aseguramiento en la muestra.",
    "NoDocbcCost": "El 8.42% dejó de consultar un médico por razones de costo, representando más de 21.000 personas que potencialmente no recibieron atención médica oportuna.",
    "DiffWalk": "El 16.82% reporta dificultad para caminar o subir escaleras. Este porcentaje otorga mayor variabilidad y potencial discriminatorio comparado con otras variables binarias.",
    "Sex": "El 55.97% son mujeres y el 44.03% hombres. La muestra presenta una leve mayoría femenina, consistente con patrones típicos de participación en encuestas de salud.",
    "Diabetes": "El 84.24% no presenta diabetes, el 13.93% tiene diabetes confirmada y apenas el 1.83% está en prediabetes. La diabetes es uno de los principales factores de riesgo cardiovascular.",
    "GenHlth": "Más de la mitad de la muestra (52.98%) califica su salud como excelente o muy buena. Solo el 4.76% la percibe como mala, sugiriendo una autopercepción generalmente positiva.",
    "Age": "Los grupos de 55-69 años concentran casi el 38% de la muestra. Los grupos jóvenes (18-29) están subrepresentados, consistente con el perfil típico del BRFSS.",
    "Education": "El 42.31% completó la universidad. La muestra está compuesta predominantemente por personas con alto nivel educativo, sesgo típico de encuestas telefónicas.",
    "Income": "El 35.63% reporta ingresos de $75.000 o más. La distribución está sesgada hacia ingresos altos, consistente con el sesgo de selección observado en educación.",
    "BMI": "El BMI presenta una media de 28.38 y mediana de 27.0, con leve asimetría positiva. El 50% central se ubica entre 24.0 y 31.0, correspondiente a peso normal alto y sobrepeso.",
    "MentHlth": "El 69.3% reportó 0 días de mala salud mental. La distribución es extremadamente asimétrica con concentración en cero y picos en valores como 7, 14 y 30 días.",
    "PhysHlth": "Similar a MentHlth, con fuerte concentración en 0 días. Los picos en 7, 14 y 30 días sugieren que quienes reportan días malos tienden a reportar semanas o el mes completo.",
}

interp_biv = {
    "HighBP": "La hipertensión muestra una de las asociaciones más fuertes con enfermedad cardíaca. Las personas con hipertensión tienen una tasa de incidencia notablemente mayor, lo que la convierte en uno de los predictores más relevantes del dataset.",
    "HighChol": "El colesterol alto presenta una asociación significativa con la enfermedad cardíaca. La tasa de incidencia en el grupo con colesterol elevado es considerablemente mayor que en el grupo sin él.",
    "CholCheck": "Quienes no se realizaron chequeo de colesterol paradójicamente muestran menor tasa de enfermedad cardíaca, posiblemente porque son personas más jóvenes y saludables que no sienten necesidad del chequeo.",
    "Smoker": "Los fumadores presentan mayor prevalencia de enfermedad cardíaca. El tabaquismo es reconocido como uno de los factores de riesgo cardiovascular modificables más importantes.",
    "Stroke": "La asociación entre ACV y enfermedad cardíaca es de las más fuertes del dataset. Quienes sufrieron un derrame cerebral tienen una tasa de incidencia cardíaca muy superior al promedio.",
    "PhysActivity": "La actividad física muestra una relación inversa con la enfermedad cardíaca: quienes no realizan actividad física tienen mayor prevalencia, confirmando su efecto cardioprotector.",
    "Fruits": "El consumo de frutas muestra una asociación modesta con menor riesgo cardíaco, aunque su efecto es menos pronunciado que factores clínicos como la hipertensión.",
    "Veggies": "Similar a Fruits, el consumo de verduras se asocia con menor prevalencia de enfermedad cardíaca, aunque con una magnitud de efecto moderada.",
    "HvyAlcoholConsump": "Sorprendentemente, el consumo alto de alcohol muestra menor tasa de enfermedad cardíaca. Esto podría explicarse por el perfil más joven de los bebedores excesivos en la muestra.",
    "AnyHealthcare": "La cobertura médica se asocia ligeramente con mayor detección de enfermedad cardíaca, posiblemente porque el acceso a salud facilita el diagnóstico.",
    "NoDocbcCost": "Las personas con barreras económicas para acceder al médico muestran mayor prevalencia de enfermedad cardíaca, reflejando el impacto del acceso a salud en los resultados cardiovasculares.",
    "DiffWalk": "La dificultad para caminar muestra una asociación fuerte con enfermedad cardíaca. Es tanto un síntoma como un factor de riesgo de deterioro cardiovascular.",
    "Sex": "Los hombres presentan mayor tasa de enfermedad cardíaca que las mujeres en esta muestra, consistente con la evidencia epidemiológica sobre mayor riesgo cardiovascular masculino.",
    "Diabetes": "La diabetes muestra una de las asociaciones más fuertes con enfermedad cardíaca. Las personas con diabetes confirmada tienen una tasa de incidencia muy superior al promedio de la muestra.",
    "GenHlth": "La autopercepción de salud es un predictor muy potente. A peor salud percibida, mayor es la tasa de enfermedad cardíaca, con una gradiente clara y consistente a lo largo de las cinco categorías.",
    "Age": "La edad muestra una relación directa y clara: a mayor grupo etario, mayor prevalencia de enfermedad cardíaca. Los grupos de 65 años en adelante concentran la mayoría de los casos.",
    "Education": "A mayor nivel educativo, menor prevalencia de enfermedad cardíaca, aunque la asociación es moderada. Esto refleja el gradiente socioeconómico en salud cardiovascular.",
    "Income": "El ingreso muestra una relación inversa con la enfermedad cardíaca: a mayores ingresos, menor prevalencia. Refuerza el papel determinante de los factores socioeconómicos en la salud cardiovascular.",
    "BMI": "El BMI es significativamente mayor en personas con enfermedad cardíaca según la prueba Mann-Whitney. Aunque la diferencia en medianas no es enorme, es estadísticamente robusta dado el tamaño de la muestra.",
    "MentHlth": "Las personas con enfermedad cardíaca reportan significativamente más días de mala salud mental. La relación entre salud cardiovascular y mental es bidireccional y clínicamente relevante.",
    "PhysHlth": "La salud física deteriorada muestra una de las asociaciones más fuertes con enfermedad cardíaca entre las variables continuas, evidenciando el impacto funcional de la enfermedad.",
}


def get_var_type(var):
    if var in continuous_vars:
        return "continua"
    elif var in ordinal_vars:
        return "ordinal"
    return "binaria"


def make_univariado_chart(var):
    vtype = get_var_type(var)

    if vtype == "continua":
        mean_val = df[var].mean()
        median_val = df[var].median()
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[var], nbinsx=40,
            marker_color="#C0392B",
            marker_line=dict(color="#0D1B2E", width=0.5),
            opacity=0.85, name=var
        ))
        fig.add_vline(x=mean_val, line_dash="dash", line_color="#E8A838",
                      annotation_text=f"Media: {mean_val:.1f}",
                      annotation_font_color="#E8A838")
        fig.add_vline(x=median_val, line_dash="dot", line_color="#4A6FA5",
                      annotation_text=f"Mediana: {median_val:.1f}",
                      annotation_font_color="#4A6FA5")
        fig.update_layout(
            **PLOT_BASE,
            title=dict(text=f"Distribución de {var}",
                       font=dict(color="#ffffff", size=14), x=0),
            xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", title=var),
            yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", title="Frecuencia"),
            height=380, showlegend=False,
        )
        return fig

    else:
        mapping = mappings.get(var, {})
        counts = df[var].value_counts().sort_index()
        labels = [mapping.get(k, str(k)) for k in counts.index]
        pcts = (counts.values / counts.sum() * 100).round(1)

        if vtype == "ordinal":
            fig = go.Figure(go.Bar(
                x=pcts, y=labels, orientation="h",
                marker=dict(
                    color=pcts,
                    colorscale=[[0, "#1a2a4a"], [1, "#C0392B"]],
                    showscale=False
                ),
                text=[f"{p}%" for p in pcts],
                textposition="outside",
                textfont=dict(color="#cbd5e1", size=11),
            ))
            fig.update_layout(
                **PLOT_BASE,
                title=dict(text=f"Distribución de {var}",
                           font=dict(color="#ffffff", size=14), x=0),
                xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8",
                           title="Porcentaje (%)", range=[0, max(pcts) * 1.2]),
                yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", autorange="reversed"),
                height=max(300, len(labels) * 45),
                showlegend=False,
            )
        else:
            fig = go.Figure(go.Bar(
                x=labels, y=pcts,
                marker=dict(
                    color=["#C0392B", "#2C3E6B"],
                    line=dict(color="#0D1B2E", width=1)
                ),
                text=[f"{p}%" for p in pcts],
                textposition="outside",
                textfont=dict(color="#cbd5e1", size=12),
            ))
            fig.update_layout(
                **PLOT_BASE,
                title=dict(text=f"Distribución de {var}",
                           font=dict(color="#ffffff", size=14), x=0),
                xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8"),
                yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8",
                           title="Porcentaje (%)", range=[0, max(pcts) * 1.2]),
                height=360, showlegend=False,
            )
        return fig


def make_bivariado_chart(var):
    vtype = get_var_type(var)
    target_map = mappings[target_var]

    if vtype == "continua":
        fig = go.Figure()
        colors_biv = ["#2C3E6B", "#C0392B"]
        for i, (val, label) in enumerate(target_map.items()):
            subset = df[df[target_var] == val][var]
            fig.add_trace(go.Box(
                y=subset, name=label,
                marker=dict(color=colors_biv[i], size=3, opacity=0.8),
                line=dict(color=colors_biv[i], width=2),
                fillcolor="rgba(13,27,46,0.8)",
                boxpoints="outliers", jitter=0,
            ))
        fig.update_layout(
            **PLOT_BASE,
            title=dict(text=f"{var} según enfermedad cardíaca",
                       font=dict(color="#ffffff", size=14), x=0),
            yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", title=var),
            xaxis=dict(color="#94a3b8", showgrid=False),
            height=380,
            legend=dict(bgcolor="#0D1B2E", bordercolor="#1e3a5f",
                        borderwidth=1, font=dict(color="#cbd5e1")),
        )
        return fig

    else:
        mapping = mappings.get(var, {})

        # ─── FIX: calcular incidencia sin groupby().apply() ───
        df_temp = df[[var, target_var]].copy()
        df_temp["var_label"] = df_temp[var].map(mapping).fillna(df_temp[var].astype(str))

        groups = df_temp["var_label"].unique()
        incidence_data = []
        for g in groups:
            mask = df_temp["var_label"] == g
            total = mask.sum()
            positivos = ((df_temp[target_var] == 1) & mask).sum()
            incidence_data.append({
                "Categoría": g,
                "Incidencia (%)": round(positivos / total * 100, 1)
            })

        incidence = pd.DataFrame(incidence_data)

        # Ordenar según mapping
        order = [mapping.get(k, str(k)) for k in sorted(mapping.keys())]
        incidence["Categoría"] = pd.Categorical(
            incidence["Categoría"], categories=order, ordered=True
        )
        incidence = incidence.sort_values("Categoría").reset_index(drop=True)

        if vtype == "ordinal":
            fig = go.Figure(go.Bar(
                x=incidence["Incidencia (%)"],
                y=incidence["Categoría"],
                orientation="h",
                marker=dict(
                    color=incidence["Incidencia (%)"].tolist(),
                    colorscale=[[0, "#1a2a4a"], [1, "#C0392B"]],
                    showscale=False,
                    line=dict(color="#0D1B2E", width=0.5)
                ),
                text=[f"{v}%" for v in incidence["Incidencia (%)"]],
                textposition="outside",
                textfont=dict(color="#cbd5e1", size=11),
            ))
            fig.update_layout(
                **PLOT_BASE,
                title=dict(text=f"Tasa de enfermedad cardíaca por {var}",
                           font=dict(color="#ffffff", size=14), x=0),
                xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8",
                           title="% con enfermedad cardíaca",
                           range=[0, incidence["Incidencia (%)"].max() * 1.25]),
                yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", autorange="reversed"),
                height=max(300, len(incidence) * 45),
                showlegend=False,
            )
        else:
            fig = go.Figure(go.Bar(
                x=incidence["Categoría"],
                y=incidence["Incidencia (%)"],
                marker=dict(
                    color=incidence["Incidencia (%)"].tolist(),
                    colorscale=[[0, "#1a2a4a"], [1, "#C0392B"]],
                    showscale=False,
                    line=dict(color="#0D1B2E", width=1)
                ),
                text=[f"{v}%" for v in incidence["Incidencia (%)"]],
                textposition="outside",
                textfont=dict(color="#cbd5e1", size=12),
            ))
            fig.update_layout(
                **PLOT_BASE,
                title=dict(text=f"Tasa de enfermedad cardíaca por {var}",
                           font=dict(color="#ffffff", size=14), x=0),
                xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8"),
                yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8",
                           title="% con enfermedad cardíaca",
                           range=[0, incidence["Incidencia (%)"].max() * 1.25]),
                height=360, showlegend=False,
            )
        return fig


def make_correlation_heatmap():
    corr = df.select_dtypes(include="number").corr()
    target_corr = corr[target_var].drop(target_var).sort_values()
    colors = ["#C0392B" if v > 0 else "#2C3E6B" for v in target_corr.values]

    fig = go.Figure(go.Bar(
        x=target_corr.values,
        y=target_corr.index,
        orientation="h",
        marker=dict(color=colors, line=dict(color="#0D1B2E", width=0.5)),
        text=[f"{v:.3f}" for v in target_corr.values],
        textposition="outside",
        textfont=dict(color="#cbd5e1", size=10),
    ))
    fig.update_layout(
        paper_bgcolor="#0D1B2E", plot_bgcolor="#0D1B2E",
        font=dict(color="#cbd5e1", family="Poppins", size=12),
        margin=dict(t=50, b=50, l=160, r=80),
        title=dict(text="Correlación de Pearson con HeartDiseaseorAttack",
                   font=dict(color="#ffffff", size=14, family="Poppins"), x=0),
        xaxis=dict(gridcolor="#1e3a5f", color="#94a3b8", title="Correlación (r)",
                   zeroline=True, zerolinecolor="#ffffff", zerolinewidth=1.5,
                   range=[target_corr.min() * 1.3, target_corr.max() * 1.3]),
        yaxis=dict(gridcolor="#1e3a5f", color="#94a3b8"),
        height=520, showlegend=False,
    )
    return fig


def compute_stats(var):
    vtype = get_var_type(var)
    if vtype == "continua":
        g0 = df[df[target_var] == 0][var]
        g1 = df[df[target_var] == 1][var]
        stat, pval = mannwhitneyu(g0, g1, alternative="two-sided")
        r = df[[var, target_var]].corr().iloc[0, 1]
        return {
            "test": "Mann-Whitney U",
            "stat": f"{stat:,.0f}",
            "pval": f"{pval:.2e}",
            "efecto": f"r = {r:.4f}",
            "efecto_label": "Correlación Pearson"
        }
    else:
        ct = pd.crosstab(df[var], df[target_var])
        chi2, pval, _, _ = chi2_contingency(ct)
        v = association(ct, method="cramer")
        return {
            "test": "Chi-cuadrado (χ²)",
            "stat": f"{chi2:,.2f}",
            "pval": f"{pval:.2e}",
            "efecto": f"V = {v:.4f}",
            "efecto_label": "V de Cramér"
        }


layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("Resultados del Análisis", style=TITLE_STYLE),
            html.Hr(style={"borderColor": "#1e3a5f", "marginTop": "1rem"}),
        ])
    ], className="mt-4"),

    # ── UNIVARIADO ──────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.H4("Análisis Univariado", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "0.3rem"
            }),
            html.P("Distribución individual de cada variable del dataset.",
                   style={**SUBTITLE_STYLE, "marginBottom": "1rem"}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="dd-uni",
                options=[{"label": v, "value": v} for v in all_vars],
                value="HighBP",
                clearable=False,
                className="dark-dropdown",
                style=DROPDOWN_STYLE
            )
        ], md=5),
        dbc.Col([
            html.Div(id="uni-tipo-badge", style={"marginTop": "0.4rem"})
        ], md=7),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id="uni-chart", config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=8),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H6("Interpretación", style={
                    "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                    "fontWeight": "700", "marginBottom": "1rem",
                    "borderBottom": "1px solid #1e3a5f", "paddingBottom": "0.5rem"
                }),
                html.Div(id="uni-interpretacion")
            ]), style={**CARD_STYLE, "height": "100%"})
        ], md=4),
    ], className="mb-5", style={"alignItems": "stretch"}),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # ── BIVARIADO ───────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.H4("Análisis Bivariado", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "0.3rem"
            }),
            html.P("Variable objetivo fija: HeartDiseaseorAttack. Selecciona la segunda variable.",
                   style={**SUBTITLE_STYLE, "marginBottom": "1rem"}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.P("Variable objetivo", style={
                    "color": "#94a3b8", "fontSize": "0.78rem",
                    "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.3rem"
                }),
                html.H6("HeartDiseaseorAttack", style={
                    "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                    "fontWeight": "700", "marginBottom": "0"
                }),
            ]), style={**CARD_STYLE, "borderColor": "#C0392B"}),
        ], md=4),
        dbc.Col([
            dcc.Dropdown(
                id="dd-biv",
                options=[{"label": v, "value": v} for v in all_vars],
                value="HighBP",
                clearable=False,
                className="dark-dropdown",
                style=DROPDOWN_STYLE
            )
        ], md=5),
        dbc.Col([
            html.Div(id="biv-tipo-badge", style={"marginTop": "0.4rem"})
        ], md=3),
    ], className="mb-4"),

    dbc.Row(id="biv-stat-cards", className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id="biv-chart", config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ], md=8),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H6("Interpretación", style={
                    "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                    "fontWeight": "700", "marginBottom": "1rem",
                    "borderBottom": "1px solid #1e3a5f", "paddingBottom": "0.5rem"
                }),
                html.Div(id="biv-interpretacion")
            ]), style={**CARD_STYLE, "height": "100%"})
        ], md=4),
    ], className="mb-5", style={"alignItems": "stretch"}),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    # ── CORRELACIÓN ─────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.H4("Correlación de Pearson con la variable objetivo", style={
                "color": "#ffffff", "fontFamily": "'Poppins', sans-serif",
                "fontWeight": "700", "marginBottom": "0.3rem"
            }),
            html.P(
                "Fuerza y dirección de la asociación lineal de cada variable con HeartDiseaseorAttack. "
                "Barras rojas indican correlación positiva y azules negativa.",
                style={**SUBTITLE_STYLE, "marginBottom": "1.5rem"}
            ),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(figure=make_correlation_heatmap(),
                          config={"displayModeBar": False})
            ]), style=CARD_STYLE)
        ])
    ], className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


@callback(
    Output("uni-chart", "figure"),
    Output("uni-interpretacion", "children"),
    Output("uni-tipo-badge", "children"),
    Input("dd-uni", "value")
)
def update_uni(var):
    fig = make_univariado_chart(var)
    texto = interp_uni.get(var, "Interpretación no disponible.")
    interpretacion = html.P(texto, style={**TEXT_STYLE, "marginBottom": "0"})
    vtype = get_var_type(var)
    color_map = {"binaria": "#C0392B", "ordinal": "#2C3E6B", "continua": "#E8A838"}
    badge = html.Span(vtype.capitalize(), style={
        "backgroundColor": color_map[vtype], "color": "#ffffff",
        "padding": "0.3rem 0.8rem", "borderRadius": "20px",
        "fontSize": "0.78rem", "fontFamily": "'Poppins', sans-serif", "fontWeight": "600"
    })
    return fig, interpretacion, badge


@callback(
    Output("biv-chart", "figure"),
    Output("biv-interpretacion", "children"),
    Output("biv-stat-cards", "children"),
    Output("biv-tipo-badge", "children"),
    Input("dd-biv", "value")
)
def update_biv(var):
    fig = make_bivariado_chart(var)
    texto = interp_biv.get(var, "Interpretación no disponible.")
    interpretacion = html.P(texto, style={**TEXT_STYLE, "marginBottom": "0"})

    stats = compute_stats(var)
    cards = [
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P(stats["test"], style={"color": "#94a3b8", "fontSize": "0.88rem",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.5rem"}),
            html.H3(stats["stat"], style={"color": "#C0392B", "fontWeight": "800",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4, className="mb-3"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("p-valor", style={"color": "#94a3b8", "fontSize": "0.88rem",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.5rem"}),
            html.H3(stats["pval"], style={"color": "#E8A838", "fontWeight": "800",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4, className="mb-3"),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.P(stats["efecto_label"], style={"color": "#94a3b8", "fontSize": "0.88rem",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0.5rem"}),
            html.H3(stats["efecto"], style={"color": "#4A6FA5", "fontWeight": "800",
                "fontFamily": "'Poppins', sans-serif", "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4, className="mb-3"),
    ]

    vtype = get_var_type(var)
    color_map = {"binaria": "#C0392B", "ordinal": "#2C3E6B", "continua": "#E8A838"}
    badge = html.Span(vtype.capitalize(), style={
        "backgroundColor": color_map[vtype], "color": "#ffffff",
        "padding": "0.3rem 0.8rem", "borderRadius": "20px",
        "fontSize": "0.78rem", "fontFamily": "'Poppins', sans-serif", "fontWeight": "600"
    })

    return fig, interpretacion, cards, badge