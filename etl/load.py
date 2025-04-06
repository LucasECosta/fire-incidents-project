from sqlalchemy import create_engine, text
from etl.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

def load_data(df, table_name="fire_incidents"):
    # Create a database engine connection
    engine = create_engine(
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )

    with engine.connect() as conn:
        # Create the table if it doesn't exist
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                "Incident Number" TEXT PRIMARY KEY,
                "Incident Date" DATE,
                "Neighborhood District" TEXT,
                "Battalion" TEXT,
                "Location" TEXT
            );
        """))
        
        # Insert each row with ON CONFLICT DO NOTHING
        for _, row in df.iterrows():
            conn.execute(text(f"""
                INSERT INTO {table_name} (
                    "Incident Number", "Incident Date", "Neighborhood District", "Battalion", "Location"
                ) VALUES (
                    :incident_number, :incident_date, :neighborhood_district, :battalion, :location
                )
                ON CONFLICT ("Incident Number") DO NOTHING;
            """), {
                'incident_number': row['incident_number'],
                'incident_date': row['incident_date'],
                'neighborhood_district': row['neighborhood_district'],
                'battalion': row['battalion'],
                'location': row.get('location', None)
            })
        
        # Validate load
        validate_data_loaded(conn, table_name)

def validate_data_loaded(conn, table_name):
    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
    count = result.scalar()
    if count == 0:
        raise ValueError("Data load failed: No records in the table.")
    else:
        print(f"✅ Data load successful: {count} records in {table_name}")

