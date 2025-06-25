import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from components.Links import linkedin, github

external_style = "assets/custom.css"

app = Dash (__name__, external_stylesheets = [external_style], use_pages=True, suppress_callback_exceptions=True)

heading = html.Div([
    html.H1('Carolina Vinado'),
    html.I('Welcome to my portfolio!'),
    ], className = 'mb-4')

header_row = dbc.Row([
        dbc.Col(
            heading,
            style={"display": "flex", "alignItems": "center"},
            width=True),
        dbc.Col(linkedin, width="auto"),
        dbc.Col(github, width="auto")
        ], align="center", className="mb-2")

app.layout = html.Div([
    header_row,
    html.Div([
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Resume", href="/Resume", active="exact"),
            dbc.NavLink("RCRD Draft Model", href="/DraftModel", active="exact"),
            dbc.NavLink("Explore Seattle", href="/ExploreSeattle", active="exact"),
            dbc.NavLink("Personal Projects", href="/PersonalProjects", active="exact"),
        ], pills=True)
    ]),
    html.Hr(),
    dash.page_container
])
app.run_server(debug= True)