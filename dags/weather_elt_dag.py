"""
dags/weather_elt_dag.py
Orkestrasi pipeline ELT Data Cuaca terjadwal harian:
1. Extract & Load raw payload via Python
2. Transform raw data ke Star Schema via dbt run
3. Uji kualitas data via dbt test
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
    "email_on_failure": False,
}

with DAG(
    dag_id="weather_data_elt_pipeline",
    default_args=default_args,
    description="Automated Daily Weather Data ELT Pipeline (Open-Meteo -> Postgres -> dbt)",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["weather", "elt", "dbt", "postgres"],
) as dag:

    # Task 1: Ekstraksi API cuaca & muat JSON mentah ke PostgreSQL
    extract_and_load = BashOperator(
        task_id="extract_and_load_weather",
        bash_command="cd /opt/airflow && python -m scripts.run_pipeline",
    )

    # Task 2: Transformasi data mentah ke Star Schema menggunakan dbt
    dbt_run = BashOperator(
        task_id="dbt_run_transformations",
        bash_command="dbt run --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project",
    )

    # Task 3: Pengujian integritas dan kualitas data menggunakan dbt test
    dbt_test = BashOperator(
        task_id="dbt_test_data_quality",
        bash_command="dbt test --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project",
    )

    # Menentukan urutan ketergantungan tugas (Dependency Pipeline)
    extract_and_load >> dbt_run >> dbt_test
