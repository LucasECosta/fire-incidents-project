# Fire Incidents ETL and Data Modeling Project - San Francisco

## About the project

This project builds a data pipeline to ingest and model fire incident data from the city of San Francisco.  
The goal is to organize this data in a data warehouse, allowing the BI team to run dynamic queries by time period, district, and battalion.

The entire process was designed following data engineering best practices, including modular code, data quality checks, deduplication strategies, and efficient modeling using dbt.

---

## Technologies used

- **Python** (pandas, sqlalchemy, dotenv)
- **PostgreSQL** (running with Docker)
- **dbt** (Data Build Tool)

---

## How to run the project

1. **Clone the repository**:

   ```bash
   git clone https://github.com/LucasECosta/fire-incidents-project.git
   cd fire-incidents-project
   ```

2. **Set up environment variables**:

   Create a `.env` file in the project root with:

   ```env
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=admin
   POSTGRES_DB=fire_incidents_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5433
   ```

3. **Start the PostgreSQL database**:

   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the ETL process**:

   ```bash
   python run_etl.py
   ```

6. **Run dbt to create the models**:

   ```bash
   cd dbt/
   dbt run
   ```

That's it! The data will be loaded and ready for analysis.

---

## Project structure

```plaintext
fire-incidents-project/
├── docker-compose.yml
├── .env
├── requirements.txt
├── run_etl.py
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── data_quality.py
│   └── config.py
├── dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── fire_incidents_base.sql
│   │   └── fire_incidents_aggregated.sql
├── reports/
│   └── report_fire_incidents_by_district.sql
└── data/
    └── fire_incidents.csv
```

---

## What was done

- **Modular ETL**: Clear separation between extraction, transformation, validation, and loading.
- **Data quality checks**: Validation for missing values and duplicates before loading the data.
- **Environment variables**: All sensitive information is handled securely through a `.env` file.
- **Robust deduplication**: Incident Number is set as a primary key, with conflict handling during insertion.
- **Modeling with dbt**: Views were created to allow easy querying by month, district, and battalion.
- **Date filtering**: Only incidents from the last 30 days are processed to optimize performance.

---

## 📝 Example report

This report shows the total number of fire incidents aggregated by:

- Month (incident_month)
- District
- Battalion

```sql
SELECT
    incident_month,
    district,
    battalion,
    total_incidents
FROM fire_incidents_aggregated
ORDER BY incident_month DESC, district, battalion;
```

You can also find this query saved in `/reports/report_fire_incidents_by_district.sql`.

---

## Final considerations

I decided to focus only on what was essential for the challenge, without adding extra features like seeds or snapshots, since they were not required for the main objective.

The entire solution was designed to ensure clean, organized, and accessible data, following good data engineering practices.

---
Feel free to reach out if you have any questions or suggestions! 


