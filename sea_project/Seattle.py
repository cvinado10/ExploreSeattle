import plotly.express as px
import geopandas as gpd
from dash import Input, Output, callback


# --LOGIC FOR THE SEATTLE MAP AND ITS CALLBACKS FOR USE IN OTHER COMPONENTS--

@callback(
    [
    Output('output-container', 'children'),
    Output('map', 'figure'),
    Output('selected-hoods', 'data'),
    ],
    [
    Input('map', 'clickData'),
    Input('map', 'selectedData'),
    Input('selected-hoods', 'data')
    ]
    )

def render (clickData, selectedData, selected_hoods):
    
    seattle = gpd.read_file('C:/Users/caro/Documents/DataScience/Notebooks/sea_project/static/Geo/Districts.geojson')
   
   
    #--DATA FILTERING THROUGH NEIGHBORHOOD SELECTION--
    
    if selected_hoods is None:
        selected_hoods = []
    
    if clickData:
        selected_hoods = [seattle.loc[point['location'], 'L_HOOD'] for point in clickData['points']]
        for hood_name in selected_hoods:
            if hood_name not in selected_hoods:
                selected_hoods.append(hood_name)
            else:
                selected_hoods.remove(hood_name)

    if selectedData:
        selected_hood_names = [seattle.loc[point['location'], 'L_HOOD'] for point in selectedData['points']]
        # Update the selected_hoods list based on multi-selection
        selected_hoods = list(set(selected_hoods + selected_hood_names))
                

    # --SELECTION DISPLAY--
    
    if selected_hoods:
        output_message = f'Current Selection: {', '.join(selected_hoods)}'
    else:
        output_message = 'Click on a neighborhood to filter data'

    
    # --MAP DISPLAY--
    
    # Build map
    seattlemap = px.choropleth_map(
        seattle, #Dataframe we're using
        geojson = seattle, #Geo data
        locations = seattle.index, #Unique identifyer needed to create shapes
        color_continuous_scale = 'sunset', #Color scale for the map geometries
        color = 'Shape__Area', #Column to determine geometries' coloring
        template = 'plotly_dark', #Template style
        center = {'lat': 47.615, 'lon': -122.34}, #Centering coordinates so the map starts at best location
        opacity = 0.4, #Opacity of the shapes
        zoom = 9.9, #Best starting zoon level for location display
        height = 500, #Sizing of feature
        )

    # Configuring hover text
    seattlemap.update_traces(
        hovertemplate = f'<b>%{{hovertext}}</b><extra></extra>', #Formatting and removing extra info on hover text (otherwise default is index and coloring)
        hovertext = seattle['L_HOOD'], #Specifying hover text to display rather than removed
        )

    # Customize and display
    seattlemap.update_layout(
        hoverlabel = {
            'font':{'color':'#F8F3EC'},
            'bordercolor':'#F8F3EC',
            'bgcolor':'#473739',
            },
        margin = {
            'r':0,
            't':0,
            'l':0,
            'b':0
            },
        coloraxis_showscale = False, #Not showing the colorscale legend
        clickmode = 'event+select', #Determine click action; set as event plus click to allow multiselection by shift+click
        activeselection_opacity = 1, #Changing opacity of clicked/nonclicked items
        selectionrevision = True, #Try to maintain current selection
        annotations=[  #Adding attribution to the map within to avoid scrollbar
            dict(
                x=1,
                y=0,
                xref='paper',
                yref='paper',
                text='© <a href="https://carto.com/about-carto/" target="_blank" rel="noopener">CARTO</a>, '
                    '© <a href="http://www.openstreetmap.org/about/" target="_blank">OpenStreetMap</a> contributors',
                showarrow=False,
                xanchor='right',
                yanchor='bottom',
                font=dict(size=10, color='white'),
                align='right'
                )
            ]
        )

    return output_message, seattlemap, selected_hoods