# Automated Weather Data ELT Pipeline

An end-to-end automated Extract, Load, Transform (ELT) data pipeline designed to ingest daily weather metrics from Open-Meteo REST API into PostgreSQL, transform raw payloads into an analytics-ready Star Schema using dbt, and orchestrate the workflow via Apache Airflow in Docker.

## Tech Stack
- **Ingestion**: Python (`requests`, `psycopg2`)
- **Data Warehouse**: PostgreSQL
- **Transformation & Modeling**: dbt-core (`dbt-postgres`)
- **Orchestration**: Apache Airflow
- **Containerization**: Docker & Docker Compose
- **Data Source**: Open-Meteo REST API

## Project Structure
