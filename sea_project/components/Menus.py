from dash import html, dcc
import dash_bootstrap_components as dbc


# --STYLING FOR THE MENUS--

# Dropdown for Topic
topic_dropdown = dcc.Dropdown(
        options = [
            {'label':'Offenses', 'value':'offenses'},
            # {'label':'Pets', 'value':'pets'},
            {'label':'Upcoming', 'value':'upcoming'},
            ],
        placeholder='Select a topic...',
        id = 'TopicDropdown',
        className = 'mb-4',
        )

topic_explanation = html.Div(id = 'explanation-container', className = 'text-secondary mb-4 d-flex flex-column')

explanation_dict = {
    'offenses' : 'Offenses reported to the Seattle Police Department (SPD). SPD started the database in 2008, and the data was cutoff at 2024 for this application. Offenses without a location or with a start date after the end date were excluded from this regional analysis. The offenses are displayed binned for the graphs, and so offenses ongoing over multiple time intervals are "counted" multiple times.',
    'pets' : 'Pets registered with the city of Seattle.',
    'upcoming' : 'As time and opportunity allows, more data will be added to this application. Stay tuned!'
    }
                 

                        

# Combined menus for the display options
topic_menus = html.Div([
        dbc.Row(html.H4('What topic do you want to explore?'),
            justify = 'center',
            align = 'center',
            ),
        dbc.Row(topic_dropdown,
            justify = 'center',
            align = 'center',
            className = 'mb-4',
            ),
        dbc.Row(topic_explanation,
            justify = 'center',
            align = 'center',
            )
        ],
        style={'maxWidth': '456px', 'margin': '0 auto'}
        )



# HERE BE DRAGONS IF MODIFIED

# RadioItems for Display
display_radioitems = dcc.RadioItems(
        options = [
            {'label':'Graphs', 'value':'graphs'},
            {'label':'Tables', 'value':'tables'},
            ],
        id = 'DisplayRadioitems',
        className = 'custom-input',
        )

# Combined menus for the display options
display_menus = html.Div([
        dbc.Row([
            dbc.Col('', style = {'width': '33%'}),
            dbc.Col(html.H3('What do you want to display?'), style = {'width': '33%'}),
            dbc.Col('', style = {'width': '33%'}),
        ]),
        dbc.Row([
            dbc.Col('', style = {'width': '33%'}),
            dbc.Col(display_radioitems, style = {'width': '33%'}),
            dbc.Col('', style = {'width': '33%'}),
        ])
        ])

# Checklist for Category
category_checklist = dcc.Checklist(
        options = [
            {'label':'Total', 'value':'Total'},
            {'label':'Person', 'value':'Person'},
            {'label':'Property', 'value':'Property'},
            {'label':'Society', 'value':'Society'},
            ],
        value = ['Total'], 
        id = 'CategoryChecklist',        
        className = 'custom-input',
        )

# Checklist for Datatype
datatype_checklist = dcc.Checklist(
        options = [
            {'label':'Absolute', 'value':'abs'},
            {'label':'Relative by Time Interval', 'value':'NT'},
            {'label':'Relative by Category', 'value':'NC'},
            ],
        value = ['abs'],
        id = 'DatatypeChecklist',
        className = 'custom-input',     
        )

# Checklist for Timeframe
timeframe_checklist = dcc.Checklist(
        options = [
            {'label':'Hour', 'value':'hour'},
            {'label':'Day-of-Week', 'value':'dow'},
            {'label':'Day', 'value':'day'},
            {'label':'Month', 'value':'month'},
            {'label':'Year', 'value':'year'},
            ],
        value = ['year'], 
        id = 'TimeframeChecklist',
        className = 'custom-input',        
        )

# Combined menus for the graphs
graph_menus = html.Div([
    dbc.Row([
        dbc.Col('', style={'width': '20%'}),
        dbc.Col(html.H4('Category:'), style = {'width': '20%'}),
        dbc.Col(html.H4('Timeframe:'), style = {'width': '20%'}),
        dbc.Col(html.H4('Data Type:'), style = {'width': '20%'}),
        dbc.Col('', style = {'width': '20%'})
    ],
    justify = 'center',
    ),
    dbc.Row([
        dbc.Col('', style = {'width': '20%'}),
        dbc.Col(datatype_checklist, style = {'width': '20%'}),
        dbc.Col(category_checklist, style = {'width': '20%'}),
        dbc.Col(timeframe_checklist, style = {'width': '20%'}),
        dbc.Col('', style = {'width': '20%'})
    ],
    justify = 'center',
    )
    ],
    id = 'graph-menus',
    className = 'mb-4'               
    )