import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


# --LOGIC FOR THE GRAPHS--

def render(app):

    @app.callback(
        Output('graphs-container', 'children'),
        [
        Input('DisplayRadioitems', 'value'),
        Input('CategoryChecklist', 'value'),
        Input('TimeframeChecklist', 'value'),
        Input('DatatypeChecklist', 'value'),
        Input('selected-hoods', 'data'),
        ],
        )
   
    def update_graphs(display, categories, timeframes, datatypes, selected_hoods):
        if display != 'graphs' or not timeframes or not categories or not datatypes:
            return []
                    
        all_graphs = []
                    
        # Dictionaries for display purposes:
        # Names for timeframe display looping
        timeframe_display_map = {
            'hour': 'Hour',
            'dow': 'DOW',
            'day': 'Day',
            'month': 'Month',
            'year': 'Year',
            }
        # Mapping dictionaries for DOWs and months
        dow_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}




        # --LOGIC FOR CHARTS--

        if not timeframes:
            return []

        for timeframe in timeframes:
            for category in categories:
                for datatype in datatypes:
                    save_dir = 'static/Created/'
                    df = pd.read_csv(os.path.join(save_dir, f'{timeframe}_crime.csv'), index_col = None)

                    if not selected_hoods:
                        df = df.loc[df['Neighborhood'] == 'Seattle']
                        df.set_index(timeframe, inplace = True)
                    elif len(selected_hoods) == 1:
                        df = df.loc[df['Neighborhood'].isin(selected_hoods)]
                        df.set_index(timeframe, inplace = True)
                    else:
                        df = df.loc[df['Neighborhood'].isin(selected_hoods)]
                        df.drop(columns = ['Neighborhood', 
                                        'NT_Person', 'NT_Property', 'NT_Society', 'NT_Total',
                                        'NC_Person', 'NC_Property', 'NC_Society', 'NC_Total',
                                        'D_Person', 'D_Property', 'D_Society', 'D_Total',
                                        'D_NT_Person', 'D_NT_Property', 'D_NT_Society', 'D_NT_Total',
                                        'D_NC_Person', 'D_NC_Property', 'D_NC_Society', 'D_NC_Total'], inplace = True)
                        df = df.groupby(timeframe).sum().reset_index()
                        normalizing_columns = ['Person', 'Property', 'Society', 'Total']
                        diff_columns = normalizing_columns + ['NT_Person', 'NT_Property', 'NT_Society', 'NT_Total', 'NC_Person', 'NC_Property', 'NC_Society', 'NC_Total']
                        def Process(df, timeframe, normalize_cols, diff_cols):
                            processed_df = []
                            # To normalize the data
                            def Normalize (df, cols):
                                def NT (df, col):
                                    return df[col]*100/df['Total']
                                def NC(df, col):
                                    return df[col]*100/df[col].sum()
                                for col in cols:
                                    df[f'NT_{col}'] = NT(df, col)
                                    df[f'NC_{col}'] = NC(df, col)
                                return df
                            # To calculate the difference between data points for waterfalls
                            def Diff(df, cols):
                                def diffy (df, col):
                                    diff_series = df[col].diff()
                                    diff_series.iloc[0] = df[col].iloc[-1] - df[col].iloc[0]
                                    return diff_series
                                for col in cols:
                                    df[f'D_{col}'] = diffy(df, col)
                                return df.round(2)
                            unit_crime = Normalize(df, normalize_cols)
                            unit_crime = Diff(df, diff_cols)
                            unit_crime = unit_crime.sort_values(by = [timeframe])
                            return unit_crime  # Return DataFrames for further use
                        # Process each time unit and save results
                        df = Process(df, timeframe, normalizing_columns, diff_columns)
                        df.set_index(timeframe, inplace = True)

                # Apply the display mappings
                    if timeframe == 'dow':
                        df['DOWs_names'] = df.index.map(dow_map)
                        df.set_index('DOWs_names', inplace=True)
                        df.index.name = 'DOW'
                    elif timeframe == 'month':
                        df['Monthly_names'] = df.index.map(month_map)
                        df.set_index('Monthly_names', inplace=True)
                        df.index.name = 'Month'
                    display_timeframe = timeframe_display_map[timeframe]
                    
                    if timeframe == 'year':
                        df = df.loc[df.index>=2008]


                    if datatype == 'abs':
                        prefix = ''
                    else:
                        prefix = f'{datatype}_'

                    # Set colors for the coloring scheme
                    sunset_colors = px.colors.sequential.Sunset
                    color_map = {
                        f'{prefix}Person':sunset_colors[4],
                        f'{prefix}Property':sunset_colors[5],
                        f'{prefix}Society':sunset_colors[6],
                        'Person':sunset_colors[4],
                        'Property':sunset_colors[5],
                        'Society':sunset_colors[6],
                        }


                    # --LOGIC FOR BAR CHART--
                    
                    if category == 'Total':
                        filtered_bar = df[[f'{prefix}Society', f'{prefix}Property', f'{prefix}Person']]
                        renamed_columns = {
                            f'{prefix}Person': 'Person',
                            f'{prefix}Property': 'Property',
                            f'{prefix}Society': 'Society',
                            f'{prefix}Total': 'Total'
                            }
                        filtered_bar = filtered_bar.rename(columns=renamed_columns)
                        bar_fig = px.bar(
                            filtered_bar,
                            x = filtered_bar.index,
                            y = filtered_bar.columns,
                            color_discrete_map = color_map,
                            opacity = 0.75,
                            )
                    else:
                        bar_fig = px.bar(
                            df,
                            x = df.index,
                            y = f'{prefix}{category}',
                            color_discrete_sequence = [color_map[f'{prefix}{category}']],
                            opacity = 0.75,
                            )
                    bar_fig.update_layout(
                        xaxis_tickangle = -45,
                        xaxis_title = f'{display_timeframe}',
                        autosize = True,
                        template = 'plotly_dark',
                        legend_title = 'Category',
                        legend_traceorder = 'reversed',
                        plot_bgcolor= 'rgba(0,0,0,0)',
                        paper_bgcolor= 'rgba(0,0,0,0)'
                        )

                    
                    
                    # --SPECIAL FORMATTING PER SETTINGS--
                    
                    if datatype == 'abs' and category == 'Total':
                        bar_fig.update_layout(
                            title = f'{category} Reported Offenses by {display_timeframe}',
                            yaxis_title = f'No. of Reported Offenses'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>No. of Reported Offenses: %{{y:.3s}}',
                            )
                    if datatype == 'abs' and category != 'Total':
                        bar_fig.update_layout(
                            title = f'Reported Offenses against {category} by {display_timeframe}',
                            yaxis_title = f'No. of Reported Offenses'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>No. of Reported Offenses: %{{y:.3s}}',
                            )
                    if datatype == 'NT' and category == 'Total':
                        bar_fig.update_layout(
                            title = f'{category} Reported Offenses Normalized per {display_timeframe}',
                            yaxis_title = f'Distribution of Reported Offenses per {display_timeframe}'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>% of Reported Offenses: %{{y:.3s}}%',
                            )
                    if datatype == 'NT' and category != 'Total':
                        bar_fig.update_layout(
                            title = f'Reported Offenses against {category} Normalized per {display_timeframe}',
                            yaxis_title = f'Distribution of Reported Offenses per {display_timeframe}'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>% of Reported Offenses: %{{y:.3s}}%',
                            )
                    if datatype == 'NC' and category == 'Total':
                        bar_fig.update_layout(
                            title = f'{category} Reported Offenses by {display_timeframe} Normalized per Category',
                            yaxis_title = f'Distribution of Reported Offenses per Category'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>% Reported Offenses: %{{y:.3s}}%',
                            )
                    if datatype == 'NC' and category != 'Total':
                        bar_fig.update_layout(
                            title = f'Reported Offenses against {category} by {display_timeframe} Normalized per Category',
                            yaxis_title = f'Distribution of Reported Offenses per Category'
                            )
                        bar_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>% Reported Offenses: %{{y:.3s}}%',
                            )
                    if datatype == 'abs' and timeframe == 'day':
                        # Make custom hover labels for day inconsistency issue
                        df['custom_hover'] = df.index.map(
                            lambda x: '<i>Lower no. of reported offenses<br>due to less months having this date<br>(February only has 29 days on leap years)</i>' if x == 29 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 30 days (February))</i>' if x == 30 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 31 days)</i>' if x == 31 else
                                ''
                            )
                        bar_fig.update_traces(
                            customdata = df['custom_hover'],
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>No. of Reported Offenses: %{{y:.3s}}<br>%{{customdata}}',
                            )
                    if datatype == 'NC' and timeframe == 'day':
                        # Make custom hover labels for day inconsistency issue
                        df['custom_hover'] = df.index.map(
                            lambda x: '<i>Lower no. of reported offenses<br>due to less months having this date<br>(February only has 29 days on leap years)</i>' if x == 29 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 30 days (February))</i>' if x == 30 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 31 days)</i>' if x == 31 else
                                ''
                            )
                        bar_fig.update_traces(
                            customdata = df['custom_hover'],
                            hovertemplate = f'{display_timeframe}: %{{x}} <br>% Reported Offenses: %{{y:.3s}}%<br>%{{customdata}}',
                            )
                    
                    # --LOGIC FOR WATERFALL CHART--
                    if category == 'Total':
                        original_col = df[f'{prefix}{category}']
                        base_category = original_col.iloc[0]
                        water_fig = go.Figure(
                            go.Waterfall(
                            x = df.index,
                            y = df[f'D_{prefix}{category}'],
                            opacity = 0.8,
                            connector = {'line':{'color': '#F8F3EC'}},
                            increasing = {'marker': {'color': sunset_colors[0]}},  # Set color for increasing bars
                            decreasing = {'marker': {'color': sunset_colors[1]}},
                            base = base_category,
                            ))
                    else:
                        original_col = df[f'{prefix}{category}']
                        base_category = original_col.iloc[0]
                        water_fig = go.Figure(
                            go.Waterfall(
                            x = df.index,
                            y = df[f'D_{prefix}{category}'],
                            base = base_category,
                            opacity = 0.8,
                            connector = {'line':{'color': '#F8F3EC'}},
                            increasing = {'marker': {'color': sunset_colors[0]}},  # Set color for increasing bars
                            decreasing = {'marker': {'color': sunset_colors[1]}},
                            ))
                    water_fig.update_layout(
                            xaxis_tickangle = -45,
                            xaxis_title = f'{display_timeframe}',
                            template = 'plotly_dark',
                            autosize = True,
                            hovermode = 'x',
                            plot_bgcolor = 'rgba(0,0,0,0)',
                            paper_bgcolor = 'rgba(0,0,0,0)'
                            )    

                    
                    # --SPECIAL FORMATTING PER SETTINGS--
                                
                    if datatype == 'abs' and category == 'Total':
                        water_fig.update_layout(
                            title= f'{category} Change in Reported Offenses by {display_timeframe}',
                            yaxis_title = f'Change in No. of Reported Offenses'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.3s}}<br>Final: %{{final:.3s}}<br>Delta: %{{delta:.3s}}<extra></extra>',
                            )
                    if datatype == 'abs' and category != 'Total':
                        water_fig.update_layout(
                            title = f'Change in Reported Offenses against {category} by {display_timeframe}',
                            yaxis_title = f'Change in No. of Reported Offenses'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.3s}}<br>Final: %{{final:.3s}}<br>Delta: %{{delta:.3s}}<extra></extra>',
                            )
                    if datatype == 'NT' and category == 'Total':
                        water_fig.update_layout(
                            title = f'{category} Change in Reported Offenses Normalized per {display_timeframe}',
                            yaxis_title = f'Change in % Reported Offenses per {display_timeframe}'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.3}}%<br>Final: %{{final:.3}}%<br>Delta: %{{delta:.3}}<extra></extra>',
                            )
                        water_fig.add_annotation(
                            xref = 'paper',
                            yref = 'paper',                
                            x = 0.5,
                            y = 0.5,
                            showarrow = False,
                            font = {
                                'size':16,
                                'color':'#F8F3EC',
                                },
                            text = 'Normalizing data by time interval totals 100%<br>each time interval and therefore no change.'
                            )
                    if datatype == 'NT' and category != 'Total':
                        water_fig.update_layout(
                            title = f'Change in Reported Offenses against {category} Normalized per {display_timeframe}',
                            yaxis_title = f'Change in % Reported Offenses per {display_timeframe}'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.2}}%<br>Final: %{{final:.2}}%<br>Delta: %{{delta:.2}}<extra></extra>',
                            )
                    if datatype == 'NC' and category == 'Total':
                        water_fig.update_layout(
                            title = f'{category} Change in Reported Offenses by {display_timeframe} Normalized per Category',
                            yaxis_title = f'Change in % Reported Offenses per Category'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.2}}%<br>Final: %{{final:.2}}%<br>Delta: %{{delta:.2}}<extra></extra>',
                            )
                    if datatype == 'NC' and category != 'Total':
                        water_fig.update_layout(
                            title = f'Change in Reported Offenses against {category} by {display_timeframe} Normalized per Category',
                            yaxis_title = f'Change in % Reported Offenses per Category'
                            )
                        water_fig.update_traces(
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.2}}%<br>Final: %{{final:.2}}%<br>Delta: %{{delta:.2}}<extra></extra>',
                            )
                    if datatype == 'abs' and timeframe == 'day':
                        # Make custom hover labels for day inconsistency issue
                        df['custom_hover_diff'] = df.index.map(
                            lambda x: '<i>Artificially higher difference in no. of<br>reported offenses due to drop in number<br>of days towards the end of the month</i>' if x==1 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(February only has 29 days on leap years)</i>' if x == 29 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 30 days (February))</i>' if x == 30 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 31 days)</i>' if x == 31 else
                                ''
                            )
                        water_fig.update_traces(
                            customdata = df['custom_hover_diff'],
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.3s}}<br>Final: %{{final:.3s}}<br>Delta: %{{delta:.3s}}<br>%{{customdata}}<extra></extra>',
                            )
                    if datatype == 'NC' and timeframe == 'day':
                        # Make custom hover labels for day inconsistency issue
                        df['custom_hover_diff'] = df.index.map(
                            lambda x: '<i>Artificially higher difference in no. of<br>reported offenses due to drop in number<br>of days towards the end of the month</i>' if x==1 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(February only has 29 days on leap years)</i>' if x == 29 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 30 days (February))</i>' if x == 30 else
                                '<i>Lower no. of reported offenses<br>due to less months having this date<br>(Not all months have 31 days)</i>' if x == 31 else
                                ''
                            )
                        water_fig.update_traces(
                            customdata = df['custom_hover_diff'],
                            hovertemplate = f'{display_timeframe}: %{{x}}<br>Initial: %{{initial:.2}}%<br>Final: %{{final:.2}}%<br>Delta: %{{delta:.2}}<br>%{{customdata}}<extra></extra>',
                            )
                    
                    graph_row = dbc.Row([
                                dbc.Col(dcc.Graph(figure = bar_fig), style = {'width': '50%'}),
                                dbc.Col(dcc.Graph(figure = water_fig), style = {'width': '50%'}),
                                ], className = 'mb-4')
                    
                    all_graphs.append(graph_row)

        return all_graphs
    
    return html.Div()