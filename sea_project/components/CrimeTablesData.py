import pandas as pd
import os



# --LOGIC FOR THE TABLES' DATA--


def process_tables(selected_hoods=None):

    save_dir = 'static/Created/'
                
    location_counts = pd.read_csv(os.path.join(save_dir, 'location_counts.csv'))
    category_counts = pd.read_csv(os.path.join(save_dir, 'category_counts.csv'))
    offense_counts = pd.read_csv(os.path.join(save_dir, 'offense_counts.csv'))
    oldest_records = pd.read_csv(os.path.join(save_dir, 'oldest.csv'))
    newest_records = pd.read_csv(os.path.join(save_dir, 'newest.csv'))
    longest_records = pd.read_csv(os.path.join(save_dir, 'longest.csv'))

    df_dict = {
        'location_counts': location_counts,
        'category_counts': category_counts,
        'offense_counts': offense_counts,
        'oldest': oldest_records,
        'newest': newest_records,
        'longest': longest_records
        }

    # Without filtering
    if not selected_hoods:        
        for key in df_dict:
            df_dict[key] = df_dict[key].loc[df_dict[key]['Hood'] == 'Seattle']

    # With filtering
    else:
        for key in df_dict:
            df_dict[key] = df_dict[key].loc[df_dict[key]['Hood'].isin(selected_hoods)]

    # Clean up formatting
    for key in df_dict:
        if not selected_hoods:
            df_dict[key] = df_dict[key].drop(columns=['Hood'])
        else:
            if 'Neighborhood' in df_dict[key].columns:
                df_dict[key] = df_dict[key].drop(columns = ['Neighborhood'])
            df_dict[key] = df_dict[key].rename(columns = {'Hood': 'Neighborhood'})

    return df_dict
