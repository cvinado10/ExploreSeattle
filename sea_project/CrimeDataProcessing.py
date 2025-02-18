# Import relevant libraries & modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from collections import defaultdict, Counter
import os


# Queried Seattle Data Project for offenses that had a reported location
# -Without associated location, data can't be displayed on the graphs, or be used for regional analysis so no reason to include it

# Queried Seattle Data Project for a geojson file of Seattle's neighborhoods



# **DATA PROCESSING**

# --PROCESS THE MAP--
# Import Geojson file
seattle = gpd.read_file('static/Geo/Districts.geojson')
# Rename Cascade to a more colloquially used name
seattle.loc[seattle['L_HOOD'] == 'Cascade', 'L_HOOD'] = 'South Lake Union'
# Drop unused columns
seattle.drop(columns = ['OBJECTID', 'S_HOOD_ALT_NAMES'], inplace = True)
# Merge geo polygons by neighborhood
seattle = seattle.dissolve(by = 'L_HOOD')
# Reset index to not have the neighborhoods as index
seattle.reset_index(inplace=True)
# Convert to projected coordinates to clean lines (buffer only works in epsg 32610)
seattle.to_crs(epsg=32610, inplace = True)
# Clean straggler lines by buffing +/- (minimun value that would buff out noticeable neighborhood merge issues)
seattle['geometry'] = seattle.buffer(0.00003).buffer(-0.00003)
# Return to geographic coordinates for compatibility with plotly
seattle.to_crs(epsg=4326, inplace = True)
# Drop unused columns
seattle.drop(columns = ['Shape__Area', 'Shape__Length'], inplace = True)


# --PROCESS THE OFFENSES--
# Import offenses file, from now on reffered to as crime for short
crime = pd.read_csv('static/Data/Crime.csv')

# Sort out formatting
# - Convert to date format
crime['Offense Start DateTime'] = pd.to_datetime(crime['Offense Start DateTime'], errors='coerce')
crime['Offense End DateTime'] = pd.to_datetime(crime['Offense End DateTime'], errors='coerce')
# Drop unused columns
crime.drop(columns = ['Report Number', 'Offense ID', 'Report DateTime', 'Group A B', 'Offense Code', 'Precinct', 'Sector', 'Beat', 'MCPP',
       '100 Block Address'], inplace = True)
# Drop the ones that start after they end
crime = crime[
    (crime['Offense Start DateTime'] <= crime['Offense End DateTime']) | 
    (crime['Offense End DateTime'].isna())
    ]
# Drop the ones that started after 2025 but keep those with no start time
crime = crime[
    (crime['Offense Start DateTime'] < pd.Timestamp('2025-01-01')) | 
    (crime['Offense Start DateTime'].isna())
    ]
# Drop the ones that ended after 2025 but keep those with no end time
crime = crime[
    (crime['Offense End DateTime'] < pd.Timestamp('2025-01-01')) | 
    (crime['Offense End DateTime'].isna())
    ]


# --JOIN DATAFRAMES--
# Stablish geometry
crime['geometry'] = crime.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis = 1)
# Convert to GeoDataFrame, and to a projected rather than geographic geometry
crime = gpd.GeoDataFrame(crime, geometry = 'geometry', crs = 'EPSG:4326')
crime = crime.to_crs('EPSG:3857')
# Convert both into the same CRS
seattle = seattle.to_crs(crime.crs)
# Join both dataframes
seattle_crime = gpd.sjoin_nearest(crime, seattle, how = 'left', distance_col = 'distance')


# --PROCESS JOINT DF--
# Formatting
# # - Convert NaT to NA for easier processing down the line
seattle_crime = seattle_crime.replace({pd.NaT: None})
# - Capitalize text instead of bloack caps
seattle_crime['Crime Against Category'] = seattle_crime['Crime Against Category'].str.capitalize()
seattle_crime['Offense Parent Group'] = seattle_crime['Offense Parent Group'].str.capitalize()
# Structural
# -Drop the non crimes (currently none have locations, but to future proof)
seattle_crime = seattle_crime[seattle_crime['Crime Against Category']!= 'Not_a_crime']
# # -Drop straggler columns
seattle_crime.drop(columns = ['index_right', 'distance'], inplace = True)
# -Sort
seattle_crime.sort_values(by = 'Crime Against Category', inplace = True)


# **DATA ANALYSIS**

# The data will be displayed binned, to deal with events that start in one bin, and end in the next, a time difference condition was included in the listing function.
# The time difference between start and end must be larger than the biggest unit could be (i.e. end day -start day >32 if we are listing the months).
# This way if the event starts in one month, but ends in the next, it will be included in both bins
# While this approach might make it seem like there are more crimes happening (the same crime will be in two bins, even if it did not occur for the majority of the bin) it was still ongoing during that bin, therefore, listed


# --DEFINE FUNCTIONS--

# To list the hours
def hours_list(row):
    start = row['Offense Start DateTime']
    end = row['Offense End DateTime']
    # If we have a start and end hour, list them all
    if pd.notna(start) and pd.notna(end): #Condition for having both a start and an end date
        if (end-start).days<0.042: #Condition for when the difference is less than an hour
            return list({start.hour, end.hour}) #List both hours
        else:
            return pd.date_range(start=start, end=end, freq = 'h').hour.to_list() #Otherwise, list all hours between the dates
    # If only start hour, list that hour
    elif pd.notna(start):
        return [start.hour]
    # If only end hour, list that hour
    elif pd.notna(end):
        return [end.hour]
    # If neither, empty list
    else:
        return []

# To list the days of week
def dows_list(row):
    start = row['Offense Start DateTime']
    end = row['Offense End DateTime']
    # If we have a start and end day, list them all
    if pd.notna(start) and pd.notna(end):
        if (end-start).days<1:
            return list({start.dayofweek, end.dayofweek})
        else:
            return pd.date_range(start=start, end=end, freq = 'D').dayofweek.to_list()
        # If only start day, list that day
    elif pd.notna(start):
        return [start.dayofweek]
    # If only end day, list that day
    elif pd.notna(end):
        return [end.dayofweek]
    # If neither, empty list
    else:
        return []

# To list the days
def days_list(row):
    start = row['Offense Start DateTime']
    end = row['Offense End DateTime']
    # If we have a start and end day, list them all
    if pd.notna(start) and pd.notna(end): #Condition for having both a start and an end day
        if (end-start).days<1: #Condition for when the difference is less than a day
            return list({start.day, end.day}) #List both days
        else:
            return pd.date_range(start=start, end=end, freq = 'D').day.to_list() #Otherwise, list all days between the dates
    # If only start day, list that day
    elif pd.notna(start):
        return [start.day]
    # If only end day, list that day
    elif pd.notna(end):
        return [end.day]
    # If neither, empty list
    else:
        return []

# To list the months
# not using month names, to simplify sorting 
def months_list(row):
    start = row['Offense Start DateTime']
    end = row['Offense End DateTime']
    # If we have a start and end month, list them all
    if pd.notna(start) and pd.notna(end):
        if (end-start).days<32:
            return list({start.month, end.month})
        else:
            return pd.date_range(start=start, end=end, freq = 'ME').month.to_list()
    # If only start day, list that day
    elif pd.notna(start):
        return [start.month]
    # If only end day, list that day
    elif pd.notna(end):
        return [end.month]
    # If neither, empty list
    else:
        return []

# To list the years
def years_list(row):
    start = row['Offense Start DateTime']
    end = row['Offense End DateTime']
    # If we have a start and end year, list them all
    if pd.notna(start) and pd.notna(end):
        # if difference is less than frequency, list begining, end, extract unique
        if (end-start).days<366:
            return list({start.year, end.year})
        else:
            return list(range(start.year, end.year+1))
    # If only start year, list that year
    elif pd.notna(start):
        return [start.year]
    # If only end year, list that year
    elif pd.notna(end):
        return [end.year]
    # If neither, empty list
    else:
        return []


# --APPLY FUNCTIONS--
time_functions = {
    'hours_list': hours_list,
    'dows_list': dows_list,
    'days_list': days_list,
    'months_list': months_list,
    'years_list': years_list
}

for column, func in time_functions.items():
    seattle_crime[column] = seattle_crime.apply(func, axis=1)



# **FURTHER ANALYSIS**


# --DEFINE FUNCTIONS--

# Function to count offenses by timeframe and neighborhood
def Count (seattle_crime, unit):
    # Drop unnecessary columns
    seattle_crime.drop(columns = ['Offense Start DateTime', 'Offense End DateTime', 'Offense Parent Group',
                              'Offense','Longitude', 'Latitude', 'geometry'])
    # Create a nested dictionary to count offenses by timeframe and category
    unit_crime_counts = defaultdict(lambda: defaultdict(lambda: Counter()))
    # Populate the counts in sequentially
    for _, row in seattle_crime.iterrows():
        event_type = row['Crime Against Category']
        neighborhood = row['L_HOOD']
        units_list = row[f'{unit}s_list']
        for u in units_list:
            unit_crime_counts[u][neighborhood][event_type] += 1
    # Flatten data
    unit_hood = []
    for u, neighborhoods in unit_crime_counts.items():
        for neighborhood, crimes in neighborhoods.items():
            row = {
                unit: u,
                'Neighborhood': neighborhood,
                'Person': crimes.get('Person', 0),
                'Property': crimes.get('Property', 0),
                'Society': crimes.get('Society', 0)
            }
            unit_hood.append(row)
    # Convert to DataFrame
    unit_crime = pd.DataFrame(unit_hood)
    unit_crime = unit_crime.sort_values(by=[unit, 'Neighborhood']).reset_index(drop=True)
    # Add total column
    unit_crime['Total'] = unit_crime[['Person', 'Property', 'Society']].sum(axis=1)
    # Add 'Seattle' w totals for ease of data pull 
    grouped_df = unit_crime.groupby(unit).sum().reset_index()
    grouped_df['Neighborhood'] = 'Seattle'
    unit_crime = pd.concat([unit_crime, grouped_df], ignore_index=True)
    return unit_crime


# Timeframes for analysis
units = ['hour', 'dow', 'day', 'month', 'year']

# Apply function
results = {unit: Count(seattle_crime, unit) for unit in units}


# Functions for further processing
def Process(df, unit, normalize_cols, diff_cols):
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
    # To apply per neighborhood for ease of data pull
    for hood in df['Neighborhood'].unique():
        subset = df[df['Neighborhood'] == hood].copy()
        normalized_subset = Normalize(subset, normalize_cols)
        diff_subset = Diff(normalized_subset, diff_cols)
        processed_df.append(diff_subset)
    unit_crime = pd.concat(processed_df, ignore_index = True)
    unit_crime = unit_crime.sort_values(by=[unit])

    return unit_crime  # Return DataFrames for further use


# Columns for the functions
normalizing_columns = ['Person', 'Property', 'Society', 'Total']
diff_columns = normalizing_columns + ['NT_Person', 'NT_Property', 'NT_Society', 'NT_Total', 
                'NC_Person', 'NC_Property', 'NC_Society', 'NC_Total']


# Process each time unit and save results
results = {unit: Process(results[unit], unit, normalizing_columns, diff_columns) for unit in units}


# Function to mass save for ease of data pull for display
def Save(df, unit):
    # File paths
    save_dir = '/static/Created/'
    crime_path = os.path.join(save_dir, f'{unit}_crime.csv')
    # Save to CSV
    df.to_csv(crime_path, index=False)

# Apply mass save
for unit in units:
    Save(results[unit], unit)

# Save Seattle Crime as well
seattle_crime.to_csv('static/Created/SeattleCrime.csv', index=False)


# **DATA FOR TABLES**

#--Pull out some high level facts for tables--


seattle_crime.rename(columns = {'L_HOOD' : 'Neighborhood'}, inplace = True)
seattle_crime['days_count'] = seattle_crime['days_list'].apply(len)
seattle_crime.drop(columns = ['Offense End DateTime', 'Offense', 'Longitude', 'Latitude', 'geometry', 'hours_list', 'dows_list', 'days_list', 'months_list', 'years_list'], inplace = True)


# Function to sort out formatting and do groupby filtering
def process_groupby(df, group_cols, drop_cols, rename_col, hood_name):
    grouped_df = df.groupby(group_cols).count().drop(columns=drop_cols)
    grouped_df.rename(columns={'Offense Start DateTime': rename_col}, inplace=True)
    grouped_df.sort_values(by=rename_col, ascending=False, inplace=True)
    grouped_df.reset_index(inplace=True)
    grouped_df['Hood'] = hood_name
    return grouped_df

# Function to pull out single records
def process_extra_records(df, sort_col, ascending, hood_name):
    record = df.sort_values(by=sort_col, ascending=ascending).iloc[:1].drop(columns=['days_count'])
    record['Hood'] = hood_name
    return record

# Initialize lists to store results
location_counts, category_counts, offense_counts = [], [], []
oldest_records, newest_records, longest_records = [], [], []

# Process Seattle-wide data
location_counts.append(process_groupby(seattle_crime, ['Neighborhood'], ['Offense Parent Group', 'Crime Against Category', 'days_count'], 'Counts', 'Seattle'))
category_counts.append(process_groupby(seattle_crime, ['Crime Against Category'], ['Neighborhood', 'Offense Parent Group', 'days_count'], 'Counts', 'Seattle'))
offense_counts.append(process_groupby(seattle_crime, ['Crime Against Category', 'Offense Parent Group'], ['Neighborhood', 'days_count'], 'Counts', 'Seattle'))
oldest_records.append(process_extra_records(seattle_crime, 'Offense Start DateTime', True, 'Seattle'))
newest_records.append(process_extra_records(seattle_crime, 'Offense Start DateTime', False, 'Seattle'))
longest_records.append(process_extra_records(seattle_crime, 'days_count', False, 'Seattle'))

# Process neighborhood-specific data
for neighborhood in seattle_crime['Neighborhood'].unique():
    neighborhood_data = seattle_crime[seattle_crime['Neighborhood'] == neighborhood]
    
    location_counts.append(process_groupby(neighborhood_data, ['Neighborhood'], ['Offense Parent Group', 'Crime Against Category', 'days_count'], 'Counts', neighborhood))
    category_counts.append(process_groupby(neighborhood_data, ['Crime Against Category'], ['Neighborhood', 'Offense Parent Group', 'days_count'], 'Counts', neighborhood))
    offense_counts.append(process_groupby(neighborhood_data, ['Crime Against Category', 'Offense Parent Group'], ['Neighborhood', 'days_count'], 'Counts', neighborhood))
    oldest_records.append(process_extra_records(neighborhood_data, 'Offense Start DateTime', True, neighborhood))
    newest_records.append(process_extra_records(neighborhood_data, 'Offense Start DateTime', False, neighborhood))
    longest_records.append(process_extra_records(neighborhood_data, 'days_count', False, neighborhood))

# Dictionary for results
results = {
    'location_counts': location_counts,
    'category_counts': category_counts,
    'offense_counts': offense_counts,
    'oldest': oldest_records,
    'newest': newest_records,
    'longest': longest_records
}

# Save to CSV
for name, data in results.items():
    pd.concat(data, ignore_index=True).to_csv(f'static/Created/{name}.csv', index=False)