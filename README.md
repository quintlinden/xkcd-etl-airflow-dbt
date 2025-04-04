# XKCD ETL Pipeline with Airflow & DBT

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

### 2. Generate the Initial Database

Run the following Python script to create the `xkcd_comics.db` database:

```bash
python fetch_xkcd_comics.py
```
When completed, make sure the `xkcd_comics.db` database is located inside the `xkcd-etl-airflow-dbt` folder.

---

### 3. Start Docker

Open Docker Desktop from your Start Menu.

Wait for it to say: **"Docker is running"**

---

### 4. Build and Start the Airflow Container

Run the following commands:

```bash
docker compose build
docker compose up
```

Wait a few minutes for Airflow to fully start.

---

### 5. Move Your DAG

Move the `fetch_new_xkcd_dag.py` file into the `dags/` folder (create it if it doesn't exist).

---

### 6. Access the Airflow UI

Once running, access Airflow at:

🔗 http://localhost:8080  
**Username:** admin  
**Password:** admin

Unpause and trigger the DAG to test if everything works.

---

### 7. Create the DBT Folder Structure

Inside the `dbt/` folder, create the following folders and move your files:

```bash
mkdir -p dbt/xkcd_transformations/models
```

Place these files in:

**`dbt/xkcd_transformations/`**  
- `dbt_project.yml`  
- `packages.yml`

**`dbt/xkcd_transformations/models/`**  
- `comic_analytics.sql`  
- `schema.yml`

---

### 8. Access the Docker Container

Open a new terminal, go to your project folder, and run:

```bash
docker exec -it airflow bash
```

---

### 9. Create the DBT Profile

This defines how DBT connects to your database:

```bash
mkdir -p /home/airflow/.dbt

cat > /home/airflow/.dbt/profiles.yml <<EOF
xkcd_transformations:
  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      database: /opt/airflow/xkcd_comics.db
      schema: main
      schemas_and_paths:
        main: /opt/airflow/xkcd_comics.db
      schema_directory: /opt/airflow
EOF
```

---

### 10. Navigate to the DBT Project Folder

```bash
cd /opt/airflow/dbt/xkcd_transformations
```

### 11. Install the Required DBT Package

```bash
dbt deps
```

### 12. Run Transformations and Tests Manually

```bash
dbt run
dbt test
```










