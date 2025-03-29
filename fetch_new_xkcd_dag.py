from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import sqlite3
import time
import os

DB_PATH = "/opt/airflow/xkcd_comics.db"  # inside the Docker container

def fetch_new_comics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comics (
            num INTEGER PRIMARY KEY,
            title TEXT,
            safe_title TEXT,
            day TEXT,
            month TEXT,
            year TEXT,
            img TEXT,
            alt TEXT,
            transcript TEXT,
            link TEXT,
            news TEXT
        );
    """)
    conn.commit()

    latest_comic = requests.get("https://xkcd.com/info.0.json").json()
    latest_num = latest_comic["num"]

    cursor.execute("SELECT MAX(num) FROM comics;")
    row = cursor.fetchone() # retrieve the result
    last_saved = row[0] if row[0] else 0 # if theres nothing in the database it will fetch from 0

    print(f"Last saved comic: {last_saved}, Latest: {latest_num}")

    new_comic_found = False # Is False, but turns True if new comic is found. Used for only running the transformation layer if a new comic is found. 

    for comic_num in range(last_saved + 1, latest_num + 1):
        url = f"https://xkcd.com/{comic_num}/info.0.json"
        try:
            response = requests.get(url)
            if response.status_code == 404:
                print(f"Comic {comic_num} not found.")
                continue
            data = response.json()

            comic_data = (
                data.get("num"),
                data.get("title"),
                data.get("safe_title"),
                data.get("day"),
                data.get("month"),
                data.get("year"),
                data.get("img"),
                data.get("alt"),
                data.get("transcript"),
                data.get("link"),
                data.get("news")
            )

            cursor.execute("""
                INSERT OR IGNORE INTO comics
                (num, title, safe_title, day, month, year, img, alt, transcript, link, news)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, comic_data)

            print(f"Saved comic #{comic_num}")
            new_comic_found = True  # Allows the Transformation Layer to run
            time.sleep(0.2)

        except Exception as e:
            print(f"Error fetching comic {comic_num}: {e}")
            continue

    conn.commit()
    conn.close()

    # Saving compute :)
    if new_comic_found:
        print("New comics found - running DBT")
        os.system("dbt run --project-dir /opt/airflow/dbt/xkcd_transformations")
        os.system("dbt test --project-dir /opt/airflow/dbt/xkcd_transformations")
    else:
        print("No new comics found - skipping DBT.")

    print("Done fetching new comics.")

# Define DAG
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="fetch_new_xkcd_comics",
    default_args=default_args,
    description="Fetch new XKCD comics and store in SQLite",
    schedule_interval="*/30 * * * 1,3,5",  # every 30 minutes on Mon, Wed, Fri (Airflow UTC timezone)
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["xkcd", "etl"],
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_new_comics_task",
        python_callable=fetch_new_comics,
    )

    fetch_task
