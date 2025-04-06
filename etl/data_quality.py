def check_data_quality(df):
    # Define critical columns that must not have nulls
    critical_columns = ['incident_number', 'incident_date', 'battalion', 'neighborhood_district']

    # Check only critical columns
    for column in critical_columns:
        null_count = df[column].isnull().sum()
        if null_count > 0:
            raise ValueError(f"Critical column '{column}' contains {null_count} null values")

    # Check for duplicate incident numbers
    if df['incident_number'].duplicated().any():
        raise ValueError("Data contains duplicate Incident Numbers")

    print("Data quality checks passed successfully!")

