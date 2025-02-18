from dash import html
import dash_bootstrap_components as dbc


# --STYLING FOR THE MAP COMPONENTS--

# Output listing current selection
output_component = html.Div(id = 'output-container', className = 'mb-4')

# Instructions for multi-selection
instruction_component = html.Div('Hold Shift while clicking for multiple selection/deselection', id = 'instruction-container', className = 'text-secondary mb-4')

# Combined map component
map_component = html.Div([
    dbc.Row(output_component),
    dbc.Row(instruction_component)
    ])