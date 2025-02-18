from dash import html, Input, Output
import dash_bootstrap_components as dbc
import dash.dash_table as dt
from components.CrimeTablesData import process_tables


# --LOGIC FOR THE TABLES' DISPLAY--

def render(app):

    tables_row = []

    @app.callback(
        Output('tables-container', 'children'),
        [
        Input('DisplayRadioitems', 'value'),
        Input('selected-hoods', 'data')
        ]
        )

    def update_tables(display, selected_hoods):
        if display != 'tables':
            return []
        
        df_dict = process_tables(selected_hoods)
        
        tables = [
            ('Counts by Neighborhood', 'location_counts', 4),
            ('Counts by Category', 'category_counts', 4),
            ('Counts by Offense', 'offense_counts', 4),
            ('Oldest Offense', 'oldest', 'auto'),
            ('Newest Offense', 'newest', 'auto'),
            ('Longest Offense', 'longest', 'auto')
        ]

        def create_table(title, key, width):
            return dbc.Col([
                html.H4(title, className='text-center'),
                html.Div(
                    dt.DataTable(
                    data=df_dict[key].to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in df_dict[key].columns],
                ),
                style={'maxWidth': '100%', 'overflowX': 'auto', 'display': 'block'}
            )
            ], width={'size': width, 'max': 12} if width == 'auto' else width, className='d-flex flex-column align-items-center')

        tables_row = html.Div([
            dbc.Row([create_table(title, key, size) for title, key, size in tables[:3]]),
            *[dbc.Row([dbc.Col(create_table(title, key, size))], className = 'mb-4') for title, key, size in tables[3:]]
        ])

        return tables_row
    
    return html.Div ()