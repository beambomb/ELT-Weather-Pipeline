# Automated Weather Data ELT Pipeline

An end-to-end automated Extract, Load, Transform (ELT) data pipeline designed to ingest daily weather metrics from Open-Meteo REST API into PostgreSQL, transform raw payloads into an analytics-ready Star Schema using dbt, and orchestrate the workflow via Apache Airflow in Docker.

---

## 🏛️ Architecture & Workflow

```text
┌────────────────┐      ┌─────────────────────────┐      ┌────────────────────────────────┐
│   Open-Meteo   │ ───> │  Python Ingestion (EL)  │ ───> │      PostgreSQL (Raw)          │
│    REST API    │      │ (Session + Auto-Retry)  │      │  raw.raw_weather_payloads      │
└────────────────┘      └─────────────────────────┘      └────────────────────────────────┘
                                                                         │
                                                                         ▼
┌────────────────────────────────────────────────────────┐       ┌───────────────┐
│              Analytics Star Schema (dbt)               │ <───  │    Staging    │
│  - fct_weather_readings (480 hourly metrics)           │       │  (Unnesting   │
│  - dim_locations (20 Indonesian cities across islands) │       │ & Dedup View) │
│  - dim_date (24-hour calendar & weekend indicator)     │       └───────────────┘
└────────────────────────────────────────────────────────┘
                           ▲
                           │ Orchestrated daily with auto-retries
┌────────────────────────────────────────────────────────┐
│             Apache Airflow (LocalExecutor)             │
│   extract_and_load ──> dbt_run ──> dbt_test            │
└────────────────────────────────────────────────────────┘
```

1. **Extract & Load (EL)**: Python script calls Open-Meteo API for 20 strategic Indonesian cities across 6 major island groups. Payloads are loaded into PostgreSQL under `raw.raw_weather_payloads` in native `JSONB` format with connection pooling and retry strategy.
2. **Transform (T)**: `dbt-core` unnests the 24-hour JSON arrays into 480 structured hourly records in the staging layer (`stg_weather_measurements`), then builds an analytical Star Schema (`fct_weather_readings`, `dim_locations`, `dim_date`).
3. **Data Quality Tests**: 18 automated dbt tests validate primary key uniqueness, not-null constraints, and referential integrity (foreign keys).
4. **Orchestration**: Apache Airflow DAG (`weather_data_elt_pipeline`) schedules daily execution, handles retries, and logs task status.
5. **Containerization**: Docker Compose manages PostgreSQL and Apache Airflow with isolated networking.

---

## 💻 Tech Stack
- **Language**: Python 3.12, SQL
- **Data Warehouse**: PostgreSQL 15
- **Data Transformation & Modeling**: dbt-core (`dbt-postgres`)
- **Orchestration**: Apache Airflow 2.9 (LocalExecutor)
- **Containerization**: Docker, Docker Compose
- **Data Source**: Open-Meteo REST API

---

## 📁 Project Structure

```text
.
├── dags/
│   └── weather_elt_dag.py         # Airflow DAG for daily scheduling
├── dbt_project/
│   ├── dbt_project.yml            # dbt configuration
│   ├── profiles.yml               # PostgreSQL connection profile
│   └── models/
│       ├── staging/
│       │   ├── sources.yml        # Raw source table declaration
│       │   └── stg_weather_measurements.sql # JSON unnesting & cleaning
│       ├── analytics/
│       │   ├── dim_locations.sql  # Location dimension (cities, island groups)
│       │   ├── dim_date.sql       # Time dimension (hours, calendar flags)
│       │   └── fct_weather_readings.sql # Fact table with hourly metrics
│       └── schema.yml             # Data quality tests (unique, not_null, relationships)
├── docker/
│   ├── Dockerfile                 # Custom Airflow image with dbt-postgres
│   └── init-db.sql                # Multi-database initializer (airflow_db, weather_dwh)
├── scripts/
│   ├── __init__.py
│   ├── config.py                  # Database configs & 20 city coordinates
│   ├── extract.py                 # Open-Meteo API client with retry mechanism
│   ├── db.py                      # PostgreSQL raw DDL and batch loader
│   └── run_pipeline.py            # Local EL pipeline entrypoint
├── .env.example                   # Environment configuration template
├── docker-compose.yaml            # Multi-container orchestration
├── requirements.txt               # Local Python dependencies
└── README.md                      # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for optional local runs)

### 2. Environment Setup
```powershell
# Copy environment variables
Copy-Item .env.example .env

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Spin Up Docker Infrastructure
```powershell
# Start PostgreSQL & Airflow (Webserver, Scheduler, Metastore)
docker compose up -d --build
```

### 4. Access Airflow Dashboard
Open your browser and navigate to:
- **URL**: [http://localhost:8080](http://localhost:8080)
- **Username**: `admin`
- **Password**: `admin`

Enable and trigger the DAG **`weather_data_elt_pipeline`** to run the complete automated pipeline!

---

## 🌟 Resume Highlights
- Designed and implemented an automated ELT pipeline extracting hourly weather metrics for 20 cities from Open-Meteo REST API into PostgreSQL using Python with connection pooling and exponential backoff retry.
- Built a dimensional Star Schema with dbt-core and implemented 18 automated data quality tests enforcing uniqueness, non-null constraints, and referential integrity.
- Orchestrated daily end-to-end task dependencies and failure retries via Apache Airflow DAGs.
- Containerized the entire infrastructure using Docker Compose with dual-database architecture for Airflow metastore and analytical data warehouse.
