FROM apache/airflow:2.9.2-python3.11

USER root
# Install dependency build dasar
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
# Install dependencies pipeline di dalam container Airflow
RUN pip install --no-cache-dir \
    requests>=2.31.0 \
    psycopg2-binary>=2.9.9 \
    dbt-postgres>=1.8.0
