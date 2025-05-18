# README.md

## 🔥 Fire Incidents Project

This project performs ingestion, transformation, and analysis of fire incident data using a comprehensive data engineering approach, involving dimensional modeling (star schema), incremental ETL pipelines, orchestration with Airflow, rigorous testing with pytest, containerized deployment, and analytical reporting with dbt.

---

## 🚀 Getting Started

### 📁 Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local execution)

### ⚙️ Setup Instructions

#### 1. Clone Repository
```bash
git clone <repo_url>
cd fire_incidents_project
```

#### 2. Environment Configuration
Copy `.env.example` to `.env` and set your variables:
```bash
cp .env.example .env
```

#### 3. Docker Deployment
Run the deployment script:
```bash
bash deploy.sh
```
Airflow will be available at: [http://localhost:8080](http://localhost:8080) (user: `admin` / password: `admin`).

#### 4. Local Execution (without Docker)
Install dependencies:
```bash
pip install -r requirements.txt
```
Run ETL scripts:
```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

### ▶️ Running dbt Transformations
```bash
docker exec -it fire_dbt dbt run --project-dir /usr/app
```

### ▶️ Running Airflow DAG
The `fire_incidents_etl` DAG is available automatically and scheduled daily. Execute and monitor via the Airflow UI.

---

## 🧱 Project Structure
```
fire_incidents_project/
├── etl/                # ETL scripts for extraction, transformation, loading
├── dbt/                # dbt models (Bronze: raw, Silver: cleaned, Gold: aggregated)
├── dags/               # Airflow DAG definitions
├── sql/                # SQL scripts for creating tables and reporting
├── metadata/           # Incremental loading metadata
├── tests/              # pytest unit tests
├── Dockerfile          # Container image for ETL pipeline
├── docker-compose.yml  # Container orchestration with PostgreSQL, ETL, dbt, Airflow
├── deploy.sh           # Infrastructure setup and container management
├── .env.example        # Template for environment configuration
└── README.md           # Project documentation
```

---

## 📐 Data Architecture & Modeling
The project follows a dimensional modeling approach using a star schema:
- **Dimension Tables**:
  - `dim_district` (district details)
  - `dim_battalion` (battalion details)
  - `dim_date` (derived from incident dates with year, month, day fields)
- **Fact Table**:
  - `fact_incident` (references the dimension tables and stores detailed incident records)

**Data Layers**:
- **Bronze**: Raw API data (minimal transformations)
- **Silver**: Cleaned, validated, and structured data
- **Gold**: Aggregated data for analytics (e.g., incident counts per month and battalion)

**PostgreSQL Optimization**:
- Partitioning by date
- Indexing frequently queried fields (`incident_number`, `incident_date`, `district`)

---

## 🔄 ETL & Orchestration

- **Incremental Load Logic**:
  - Tracks last loaded timestamp (`updated_at`) in metadata.
  - ETL scripts fetch only new or updated records.
  - Deduplication ensures already ingested records (`incident_number`) are skipped.

- **Airflow Orchestration**:
  - Manages ETL tasks with dependencies (`extract` → `transform` → `load` → `dbt`).
  - Implements retries and detailed logging with the Python `logging` module.
  - Scheduled daily for automated execution.

- **Error Handling & Retry Logic**:
  - Exception-specific error handling (`try/except`).
  - Exponential backoff for API and database retries.
  - psycopg2 transactions with rollback on errors.

---

## ✅ Data Validation & Testing
- **Data Quality Checks**:
  - Validation of mandatory fields (`incident_number`, `incident_date`, `location`).
  - Rejection or quarantine of invalid data rows before loading.
  - Preservation of business logic (unique incident numbers).

- **pytest Unit Tests**:
  - Each transformation step tested against realistic edge cases.
  - Deduplication and time-based filtering specifically tested.
  - Fixtures included for simulating API responses.

---

## 🚢 DevOps & Deployment Practices

- **Full Dockerization**:
  - Dockerfiles and `docker-compose.yml` for the ETL pipeline, PostgreSQL, dbt, and Airflow.

- **Secure Environment Variables**:
  - No hardcoded credentials; configurations are managed via `.env`.

- **Deployment Automation**:
  - `deploy.sh` script automates infrastructure setup and container orchestration.

---

## 📈 Reporting & Business Insight

### Advanced Incident Report
Stored as a dbt model (`gold/incidents_by_month.sql`), provides monthly incident counts by battalion:
```sql
SELECT battalion_name, DATE_TRUNC('month', incident_date) AS month, COUNT(*)
FROM fact_incident
GROUP BY 1, 2;
```

**Report Value**: Essential for fire department leadership and public safety analysts, supporting strategic decision-making in resource allocation and emergency preparedness planning.

---

## 🗺 System Architecture Diagram
```
[Public API] → [Python ETL (Incremental, Validations)] → [PostgreSQL (Star Schema)] → [dbt (Transformations)] → [Analytics Reports]
```

---
