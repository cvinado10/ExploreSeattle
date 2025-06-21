from dash import html
import dash_bootstrap_components as dbc


# --STYLING FOR THE LAYOUT HEADERS--

# Header
heading = html.Div([
    html.H2('Explore Seattle!'),
    html.H3('A Data Visualization Application'),
    ],
    className = 'mb-4',
    )

# Map title
map_heading = html.Div([
    dbc.Row([
        dbc.Col(html.H3("Seattle's Neighborhoods"), width = 'auto'),
        ],
        justify = 'center',
        align = 'center',
        )
    ],
    )