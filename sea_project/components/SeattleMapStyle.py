from dash import dcc


# --STYLING FOR THE MAP--

seattle_map = dcc.Graph(
    id = 'map',
    config = {
        'scrollZoom': False,
        'displayModeBar': False,
        'displaylogo': False,
    },
    style = {
        'width': '100%',
        'aspectRatio': '1 / 1',
        'max-width': '500px',
        'margin': 'auto',
        },
    className = 'map-container',
    )