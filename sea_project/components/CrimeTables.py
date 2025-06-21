import os
import pandas as pd
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash.dash_table as dt

# --LOGIC FOR THE TABLES' DATA--
def process_tables(selected_hoods=None):
    save_dir = 'static/Created/'
    
    df_dict = {
        'location_counts': pd.read_csv(os.path.join(save_dir, 'location_counts.csv')),
        'category_counts': pd.read_csv(os.path.join(save_dir, 'category_counts.csv')),
        'offense_counts': pd.read_csv(os.path.join(save_dir, 'offense_counts.csv')),
        'oldest': pd.read_csv(os.path.join(save_dir, 'oldest.csv')),
        'newest': pd.read_csv(os.path.join(save_dir, 'newest.csv')),
        'longest': pd.read_csv(os.path.join(save_dir, 'longest.csv'))
        }

    # Apply filtering
    if not selected_hoods:
        for key in df_dict:
            df_dict[key] = df_dict[key].loc[df_dict[key]['Hood'] == 'Seattle']
    else:
        for key in df_dict:
            df_dict[key] = df_dict[key].loc[df_dict[key]['Hood'].isin(selected_hoods)]
    
    # Clean up formatting
    for key in df_dict:
        if not selected_hoods:
            df_dict[key] = df_dict[key].drop(columns=['Hood'])
        else:
            if 'Neighborhood' in df_dict[key].columns:
                df_dict[key] = df_dict[key].drop(columns=['Neighborhood'])
            df_dict[key] = df_dict[key].rename(columns={'Hood': 'Neighborhood'})
    
    return df_dict

# --LOGIC FOR THE TABLES' DISPLAY--
def render():
    html.Div(id='tables-container')
    
@callback(
    Output('tables-container', 'children'),
    [Input('DisplayRadioitems', 'value'), Input('selected-hoods', 'data')]
    )
def update_tables(display, selected_hoods):
    if display != 'tables':
        return []
    
    df_dict = process_tables(selected_hoods)
    
    tables = [
        ('Counts by Neighborhood', 'location_counts', 'auto'),
        ('Counts by Category', 'category_counts', 'auto'),
        ('Counts by Offense', 'offense_counts', 'auto'),
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
        ], width={'size': width, 'max': 12}, className='d-flex flex-column align-items-center')
    
    tables_row = html.Div([
        dbc.Row([dbc.Col(create_table(title, key, size))], className='mb-4') for title, key, size in tables
        ])
    
    return tables_row