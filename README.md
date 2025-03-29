# xkcd-etl-airflow-dbt
ETL pipeline for XKCD comics using Python, Airflow, DBT, and SQLite.

# 📊 XKCD ETL Pipeline with Airflow & DBT

**Beginner guide to creating a data pipeline for XKCD comics using Apache Airflow, DBT, and Docker.**

This project fetches comic metadata from the XKCD API, stores it in a SQLite database, transforms the data using DBT, and automates everything with Airflow inside Docker.

---

## Getting Started

### 1. Clone the Project

Open an **empty folder**, then run:

```bash
git clone https://github.com/quintlinden/xkcd-etl-airflow-dbt.git
cd xkcd-etl-airflow-dbt
```

---

## 2. Generate the Initial Database

Run the following Python script to create the `xkcd_comics.db` database:

\`\`\`bash
python fetch_xkcd_comics.py
\`\`\`

When completed, make sure the `xkcd_comics.db` database is located inside the `xkcd-etl-airflow-dbt` folder.

