import pandas as pd

def transform_data(df):
    # Step 1: Normalize column names
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    
    # Step 2: Drop rows missing critical information
    df = df.dropna(subset=['incident_number', 'incident_date', 'battalion', 'neighborhood_district'])
    
    # Step 3: Remove duplicate incidents
    df = df.drop_duplicates(subset=['incident_number'])
    
    # Step 4: Convert date columns to datetime
    date_columns = [
        'incident_date', 'alarm_dttm', 'arrival_dttm', 'close_dttm', 
        'data_as_of', 'data_loaded_at'
    ]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Step 5: Drop rows where Incident Date conversion failed
    df = df.dropna(subset=['incident_date'])
    
    # Step 6: Fill missing values for less critical columns (numerical)
    numerical_columns = ['supervisor_district', 'zipcode', 'station_area', 'box']
    for col in numerical_columns:
        if col in df.columns:
            if col == 'box':
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna(-1).astype(int, errors='ignore')
    
    # Step 7: Fill string columns with "Unknown"
    string_columns = [
        'city', 'primary_situation', 'mutual_aid', 'action_taken_primary', 
        'action_taken_secondary', 'action_taken_other', 'property_use',
        'area_of_fire_origin', 'ignition_cause', 'ignition_factor_primary', 
        'ignition_factor_secondary', 'heat_source', 'item_first_ignited',
        'human_factors_associated_with_ignition', 'structure_type',
        'structure_status', 'neighborhood_district'
    ]
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
    
    # Step 8: Replace 'NA' values
    df = df.replace('NA', 'Unknown')
    
    # Step 9: Filter for last 30 days
    today = pd.to_datetime('today')
    cutoff_date = today - pd.Timedelta(days=30)
    df = df[df['incident_date'] >= cutoff_date]

    return df

