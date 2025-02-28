from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from components import CrimeTables, CrimeGraphs
from components.Explore import heading, map_heading
from components.MapComponent import map_component
from components.SeattleMapStyle import seattle_map
from components.Menus import display_menus, graph_menus, topic_menus, explanation_dict
from components.Links import linkedin, github, sources


# --LOGIC FOR THE LAYOUT--

def create_layout(app):
    # Define the callback for both toggling visibility and updating the explanation
    @app.callback(
    [
        Output('offense-container', 'style'),  # Controls visibility of everything
        Output('conditional-graphs-options', 'style'),
        Output('conditional-graph', 'style'),  
        Output('conditional-table', 'style'),
        Output('explanation-container', 'children')  # Keep explanation functionality
    ],
    [
        Input('TopicDropdown', 'value'),
        Input('DisplayRadioitems', 'value')
    ]
    )
    
    def update_layout(selected_topic, display):
        
        # Explanation of the database
        explanation = explanation_dict.get(selected_topic)

        # If TopicDropdown is not "offenses", hide offense-container but keep explanation
        if selected_topic != 'offenses':
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, explanation

        # Otherwise, show offense-container and handle table/graph visibility
        if display is None or display == 'tables':
            return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, explanation
        else:
            return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, explanation


    # --STYLING FOR THE LAYOUT SECTIONS--

    links_row = html.Div([
        dbc.Row(sources),
        dbc.Row([
            dbc.Col(linkedin, width='auto'),
            dbc.Col(github, width='auto')
        ]),
        ],
        className='g-2',
        style={
            'top': '10px',
            'right': '10px',
            'gap': '10px',
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'flex-end'
            })


    explore_row = html.Div([
        dbc.Row(heading),
        dbc.Row(map_heading),
        ],
        )


    map_row = dbc.Row([
        dbc.Col(topic_menus, style={'width': '33%', 'display': 'flex', 'justify-content': 'center', 'overflow': 'hidden'}, className='align-self-start'),
        dbc.Col(seattle_map, style={'width': '33%', 'display': 'flex', 'justify-content': 'center', 'overflow': 'hidden'}),
        dbc.Col(map_component, style={'width': '33%'}),
        dcc.Store(id='selected-hoods', data=[])
    ], justify='center', align='center', className='mb-4')


    display_options = dbc.Row(display_menus,
        justify = 'center',
        align = 'center',
        id='display-options'
        )


    tables_results = dbc.Row([
        dbc.Col(CrimeTables.render(app), style={'width': '100%'}, id='tables-container'),
        ], id='conditional-table')


    graphs_options = dbc.Row(graph_menus,
        justify = 'center',
        align = 'center',
        id = 'conditional-graphs-options'
        )


    graphs_results = dbc.Row([
        dbc.Col(CrimeGraphs.render(app), style={'width': '100%'}, id = 'graphs-container'),
        ], id='conditional-graph')

    offense_container = html.Div([
        display_options,
        # Sub-container for tables & graphs, controlled by DisplayRadioitems
        html.Div([
            tables_results,
            graphs_options,
            graphs_results
        ], id='tables-graphs-container')
        ], id='offense-container')

    # --LAYOUT--

    layout = html.Div(
    dbc.Container([
        links_row,
        explore_row,
        map_row,
        offense_container
    ],
    fluid=True),
    className='bg-body',
    **{'data-bs-theme': 'dark'}
    )

    return layout