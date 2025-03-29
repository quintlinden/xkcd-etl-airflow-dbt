import requests  # for making HTTP requests to the API
import sqlite3   # for working with a local SQLite database
import time      # to pause between API calls

# Connect to (or create) the local database
conn = sqlite3.connect("xkcd_comics.db")  # this will create a file if it doesn't exist
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Save changes to the database
conn.commit()

# Step 1: Get the latest comic number
LATEST_COMIC_URL = "https://xkcd.com/info.0.json"

try:
    response = requests.get(LATEST_COMIC_URL)
    response.raise_for_status() # will raise exception if request was not succesful (error)
    latest_comic_data = response.json()
    latest_num = latest_comic_data["num"]
    print(f"Latest XKCD comic number is: {latest_num}")
except Exception as e: # handles if there was request error
    print(f"Error fetching latest comic: {e}")
    conn.close()
    exit(1)

# Step 2: Loop through all comic numbers and insert into DB
for comic_num in range(1, latest_num + 1):
    comic_url = f"https://xkcd.com/{comic_num}/info.0.json"
    
    try:
        response = requests.get(comic_url)
        if response.status_code == 404: # most common error
            print(f"Comic {comic_num} not found (404). Skipping.")
            continue

        response.raise_for_status() # will raise exception if request was not succesful (error)
        data = response.json()

        # Extract relevant fields
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

        # Insert into DB (ignore if comic already exists in DB): for when script is re-run
        cursor.execute("""
            INSERT OR IGNORE INTO comics 
            (num, title, safe_title, day, month, year, img, alt, transcript, link, news)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, comic_data)

        print(f"Saved comic #{comic_num}") # REMOVE for terminal cluttering

        # Prevent API hammering: 200 milliseconds delays inbetween calls
        time.sleep(0.2)

    except Exception as e: # handling other types of error
        print(f"Error with comic #{comic_num}: {e}")
        continue

# Final commit and close
conn.commit()
conn.close()
print("All comics fetched and saved")


