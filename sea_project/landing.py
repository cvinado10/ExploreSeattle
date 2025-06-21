import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from components.Links import linkedin, github

# --LOGIC FOR THE LANDING LAYOUT--

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


def create_layout(app):
    layout = html.Div([
        dcc.Location(id="url"),
        header_row,
        dcc.Link("Home", href="/"),
        " | ",
        dcc.Link("Resume", href="/Resume"),
        " | ",
       dcc.Link("RCRD Draft Model", href="/DraftModel"),
        " | ",
        dcc.Link("Explore Seattle", href="/ExploreSeattle"),
        " | ",
        dcc.Link("Personal Projects", href="/PersonalProjects"),
        html.Hr(),
        dash.page_container
        ])

    return layout