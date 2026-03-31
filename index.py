import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app

from dash import page_container

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Inicio",         href="/")),
        dbc.NavItem(dbc.NavLink("Objetivos",      href="/objetivos")),
        dbc.NavItem(dbc.NavLink("Marco Teórico",  href="/marco-teorico")),
        dbc.NavItem(dbc.NavLink("Metodología",    href="/metodologia")),
        dbc.NavItem(dbc.NavLink("Carga",          href="/carga")),
        dbc.NavItem(dbc.NavLink("Limpieza",       href="/limpieza")),
        dbc.NavItem(dbc.NavLink("Resultados",     href="/resultados")),
        dbc.NavItem(dbc.NavLink("Síntesis",       href="/sintesis")),
        dbc.NavItem(dbc.NavLink("Referencias",    href="/referencias")),
    ],
    brand="",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
)

app.layout = html.Div([
    navbar,
    page_container
], style={"backgroundColor": "#152b46", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True)
    