import dash
from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Inicio")

layout = dbc.Container([

    # Título principal
    dbc.Row([
        dbc.Col([
            html.H1(
                "Factores asociados a enfermedades cardíacas - encuesta BRFSS 2015",
                style={
                    "color": "#ffffff",
                    "fontWeight": "800",
                    "fontSize": "2.2rem",
                    "borderLeft": "6px solid #C0392B",
                    "paddingLeft": "16px",
                    "marginTop": "2rem",
                    "fontFamily": "'Poppins', sans-serif"
                }
            ),
            html.H5(
                "Análisis Exploratorio de Indicadores de Salud",
                style={
                    "color": "#94a3b8",
                    "marginBottom": "1.5rem",
                    "marginTop": "0.5rem",
                    "fontFamily": "'Poppins', sans-serif",
                    "fontWeight": "300"
                }
            ),
            html.Hr(style={"borderColor": "#1e3a5f"}),
        ])
    ]),

    # Introducción + métricas
    dbc.Row([
        dbc.Col([
            html.P(
                "Las enfermedades cardíacas representan la principal causa de muerte en "
                "Estados Unidos, cobrando aproximadamente 647.000 vidas cada año y generando "
                "una de las mayores cargas económicas y sanitarias del país. A diferencia de "
                "otras enfermedades, la cardiopatía coronaria avanza de forma silenciosa: la "
                "acumulación de placa en las arterias, la inflamación crónica, la hipertensión "
                "y la diabetes deterioran el sistema cardiovascular durante años antes de que "
                "aparezca cualquier síntoma visible.",
                style={
                    "color": "#cbd5e1",
                    "fontSize": "0.97rem",
                    "lineHeight": "1.9",
                    "textAlign": "justify",
                    "fontFamily": "'Poppins', sans-serif"
                }
            ),
            html.P(
                "En este contexto, las encuestas poblacionales de salud representan una fuente "
                "valiosa de información. El Sistema de Vigilancia de Factores de Riesgo "
                "Conductuales (BRFSS), administrado anualmente por el CDC desde 1984, recoge "
                "respuestas de más de 400.000 estadounidenses sobre conductas de riesgo, "
                "enfermedades crónicas y uso de servicios preventivos.",
                style={
                    "color": "#cbd5e1",
                    "fontSize": "0.97rem",
                    "lineHeight": "1.9",
                    "textAlign": "justify",
                    "fontFamily": "'Poppins', sans-serif"
                }
            ),
            html.P(
                "El dataset empleado corresponde a la versión depurada del BRFSS 2015, con "
                "253.680 registros y 22 variables que incluyen indicadores como el índice de "
                "masa corporal, actividad física, tabaquismo, consumo de alcohol, presión "
                "arterial, colesterol, diabetes, acceso a atención médica y características "
                "sociodemográficas como edad, sexo, nivel educativo e ingreso del hogar.",
                style={
                    "color": "#cbd5e1",
                    "fontSize": "0.97rem",
                    "lineHeight": "1.9",
                    "textAlign": "justify",
                    "fontFamily": "'Poppins', sans-serif"
                }
            ),
        ], md=8, style={"display": "flex", "flexDirection": "column"}),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("253.680",
                        style={"color": "#C0392B", "fontWeight": "800",
                               "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
                    html.P("Registros en el dataset",
                        style={"textAlign": "center", "color": "#94a3b8",
                               "fontSize": "0.85rem", "marginBottom": "1.5rem"}),

                    html.H3("22",
                        style={"color": "#98033F", "fontWeight": "800",
                               "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
                    html.P("Variables analizadas",
                        style={"textAlign": "center", "color": "#94a3b8",
                               "fontSize": "0.85rem", "marginBottom": "1.5rem"}),

                    html.H3("9.42%",
                        style={"color": "#E8A838", "fontWeight": "800",
                               "textAlign": "center", "fontFamily": "'Poppins', sans-serif"}),
                    html.P("Prevalencia de enfermedad cardíaca",
                        style={"textAlign": "center", "color": "#94a3b8",
                               "fontSize": "0.85rem", "marginBottom": "0"}),
                ], style={
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "height": "100%"
                })
            ], style={
                "backgroundColor": "#0D1B2E",
                "border": "1px solid #1e3a5f",
                "borderRadius": "12px",
                "height": "100%"
            })
        ], md=4, style={"display": "flex", "flexDirection": "column"}),

    ], className="mb-5", style={"alignItems": "stretch"}),

    html.Hr(style={"borderColor": "#1e3a5f"}),

    
    # Iconos Watch video + About us
    dbc.Row([

        # YouTube
        # dbc.Col([
        #     html.A([
        #         html.Img(
        #             src="/assets/youtube-svgrepo-com.svg",
        #             style={
        #                 "width": "48px",
        #                 "height": "48px",
        #                 "filter": "brightness(0) invert(1)"
        #             }
        #         ),
        #         html.P("Watch video",
        #             style={
        #                 "color": "#E7E9EC",
        #                 "fontSize": "0.88rem",
        #                 "marginTop": "0.5rem",
        #                 "marginBottom": "0",
        #                 "fontFamily": "'Poppins', sans-serif"
        #             })
        #     ],
        #     href="https://youtu.be/Exgc-QKA22Q?list=RDExgc-QKA22Q",
        #     target="_blank",
        #     style={
        #         "textDecoration": "none",
        #         "textAlign": "center",
        #         "display": "flex",
        #         "flexDirection": "column",
        #         "alignItems": "center",
        #         "cursor": "pointer"
        #     })
        # ], md=2, style={"display": "flex", "justifyContent": "center"}),
        
        dbc.Col([
            html.A([
                html.Img(
                    src="/assets/code-fork-svgrepo-com.svg",
                    style={
                        "width": "48px",
                        "height": "48px",
                        "filter": "brightness(0) invert(1)"
                        }
                    ),
                html.P("Dataset",
                       style={
                           "color": "#E7E9EC",
                            "fontSize": "0.88rem",
                            "marginTop": "0.5rem",
                            "marginBottom": "0",
                            "fontFamily": "'Poppins', sans-serif"
                            })
                ],
                   href="https://www.kaggle.com/datasets/alexteboul/heart-disease-health-indicators-dataset/data",
                   target="_blank",
                   style={
                       "textDecoration": "none",
                        "textAlign": "center",
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "cursor": "pointer"
                        })
            ], md=2, style={"display": "flex", "justifyContent": "center"}),
        
        


        # About us
        dbc.Col([
            html.Div([
                html.Img(
                    src="/assets/people-svgrepo-com.svg",
                    style={
                        "width": "48px",
                        "height": "48px",
                        "filter": "brightness(0) invert(1)",
                        "cursor": "pointer"
                    }
                ),
                html.P("About us",
                    style={
                        "color": "#E7E9EC",
                        "fontSize": "0.88rem",
                        "marginTop": "0.5rem",
                        "marginBottom": "0",
                        "fontFamily": "'Poppins', sans-serif"
                    })
            ],
            id="about-trigger",
            style={
                "textAlign": "center",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "cursor": "pointer"
            },
            n_clicks=0),

            # Modal colaboradores
            dbc.Modal([
                dbc.ModalHeader(
                    html.H5("Colaboradores",
                            style={
                                "fontFamily": "'Poppins', sans-serif",
                                "fontWeight": "700",
                                "color": "#ffffff",
                                "marginBottom": "0"
                                }),
                    style={"backgroundColor": "#0D1B2E", "borderBottom": "1px solid #1e3a5f"}
                    ),
                dbc.ModalBody([

                    dbc.Row([
                        dbc.Col([
                            html.Img(
                                src="/assets/person-svgrepo-com.svg",
                                style={"width": "36px", "filter": "brightness(0) invert(1)"}
                            ),
                        ], width=2, style={"display": "flex", "alignItems": "center"}),
                        dbc.Col([
                            html.P("Natalia Alvarado",
                                style={
                                    "color": "#ffffff",
                                    "fontWeight": "600",
                                    "marginBottom": "0.1rem",
                                    "fontFamily": "'Poppins', sans-serif"
                                }),
                            html.A("github.com/paolacorr67-ctrl",
                                href="https://github.com/paolacorr67-ctrl",
                                target="_blank",
                                style={"color": "#C0392B", "fontSize": "0.85rem",
                                       "textDecoration": "none"})
                        ])
                    ], className="mb-4"),

                    dbc.Row([
                        dbc.Col([
                            html.Img(
                                
                                src="/assets/person-svgrepo-com.svg",
                                style={"width": "36px", "filter": "brightness(0) invert(1)"}
                            ),
                        ], width=2, style={"display": "flex", "alignItems": "center"}),
                        dbc.Col([
                            html.P("Camilo Mujica",
                                style={
                                    "color": "#ffffff",
                                    "fontWeight": "600",
                                    "marginBottom": "0.1rem",
                                    "fontFamily": "'Poppins', sans-serif"
                                }),
                            html.A("github.com/camilo-mujica",
                                href="https://github.com/camilo0709",
                                target="_blank",
                                style={"color": "#C0392B", "fontSize": "0.85rem",
                                       "textDecoration": "none"})
                        ])
                    ]),

                ], style={"backgroundColor": "#0D1B2E"}),

                dbc.ModalFooter(
                    dbc.Button("Cerrar", id="close-modal", color="danger", size="sm"),
                    style={"backgroundColor": "#0D1B2E", "borderTop": "1px solid #1e3a5f"}
                ),
            ],
            id="about-modal",
            is_open=False,
            centered=True),

        ], md=2, style={"display": "flex", "justifyContent": "center"}),

    ], justify="center", className="mb-5"),

], fluid=True, style={"padding": "2rem 3rem", "backgroundColor": "#070E1A"})


@callback(
    Output("about-modal", "is_open"),
    Input("about-trigger", "n_clicks"),
    Input("close-modal", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(n1, n2):
    from dash import ctx
    if ctx.triggered_id == "about-trigger":
        return True
    return False