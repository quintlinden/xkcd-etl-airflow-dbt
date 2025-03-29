FROM apache/airflow:2.8.1-python3.10

USER airflow

RUN pip install --no-cache-dir \
    dbt-core==1.5.5 \
    dbt-sqlite==1.5.1
