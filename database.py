import sqlite3
import time
from gms import GMS

# Database setup
def init_db():
    conn = sqlite3.connect("greenhouse.db")
    cursor = conn.cursor()
    # Create a table to store sensor data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        distance REAL
    )
    """)
    conn.commit()
    conn.close()

# Function to save data to the database
def save_to_db(temperature, humidity, distance):
    conn = sqlite3.connect("greenhouse.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO sensor_data (timestamp, temperature, humidity, distance)
    VALUES (datetime('now'), ?, ?, ?)
    """, (temperature, humidity, distance))
    conn.commit()
    conn.close()

# Main function to fetch and save data
def monitor_sensors():
    gms = GMS()  # Initialize the GMS object

    while True:
        try:
            # Get temperature and humidity
            humidity, temperature = gms.get_temp_hum()

            # Get distance from sonar sensor
            distance = gms.get_distance()

            # Save data to the database
            save_to_db(temperature, humidity, distance)
            print(f"Saved: Temp={temperature}°C, Hum={humidity}%, Distance={distance}cm")

            # Wait for a specified interval before the next read (e.g., 10 seconds)
            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    init_db()  # Initialize the database
    monitor_sensors()  # Start monitoring
