from flask import Flask, request, jsonify
import threading
import time
from gms import GMS
import sqlite3
from database import *

app = Flask(__name__)

# Mock database for REST API
greenhouse_data = {
    "sensors": {
        "temperature": 25.5,
        "humidity": 60,
        "soil_moisture": 40,
        "light": 300,
        "soilMoisture": 1,
        "tvoc": 0,
        "co2": 0
    },
    "controls": {
        "water_pump": "OFF",
        "ventilation": "OFF",
    },
}

# Route: Get all sensor data from the database
@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    try:
        conn = sqlite3.connect("greenhouse.db")
        cursor = conn.cursor()

        # Query the latest sensor data
        cursor.execute("""
        SELECT timestamp, temperature, humidity, distance, soil_moisture, tvoc, co2 
        FROM sensor_data 
        ORDER BY id DESC LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()

        if row:
            timestamp, temperature, humidity, distance, soil_moisture, tvoc, co2 = row
            return jsonify({
                "timestamp": timestamp,
                "temperature": temperature,
                "humidity": humidity,
                "distance": distance,
                "soilMoisture": soil_moisture,
                "tvoc": tvoc,
                "co2": co2
            }), 200
        else:
            return jsonify({"error": "No sensor data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Update specific sensor data (mock update)
@app.route('/api/sensors/<sensor_name>', methods=['PUT'])
def update_sensor_data(sensor_name):
    if sensor_name in greenhouse_data['sensors']:
        data = request.json
        greenhouse_data['sensors'][sensor_name] = data.get('value', greenhouse_data['sensors'][sensor_name])
        return jsonify({sensor_name: greenhouse_data['sensors'][sensor_name]}), 200
    return jsonify({"error": "Sensor not found"}), 404

# Route: Get control device status
@app.route('/api/controls', methods=['GET'])
def get_controls():
    return jsonify(greenhouse_data['controls']), 200

# Route: Update control device state
@app.route('/api/controls/<device_name>', methods=['PUT'])
def update_control(device_name):
    if device_name in greenhouse_data['controls']:
        data = request.json
        greenhouse_data['controls'][device_name] = data.get('state', greenhouse_data['controls'][device_name])
        return jsonify({device_name: greenhouse_data['controls'][device_name]}), 200
    return jsonify({"error": "Device not found"}), 404

# Route: Ping (for health check)
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Greenhouse API is up and running!"}), 200

# Sensor monitoring function
def monitor_sensors():
    global greenhouse_data
    gms = GMS()  # Initialize the GMS object

    while True:
        try:
            # Get temperature and humidity
            temperature, humidity = gms.get_temp_hum()

            # Get distance from sonar sensor
            distance = gms.get_distance()

            # Get soil moisture
            soil_moisture = gms.soilMoisture()

            # Get air quality
            air_quality = gms.AirQuality()
            tvoc, co2 = air_quality

            # Save data to the database
            save_to_db(temperature, humidity, distance, soil_moisture, tvoc, co2)

            print(f"Saved: Temp={temperature}°C, Hum={humidity}%, Distance={distance}cm, "
                  f"SoilMoisture={soil_moisture}, TVOC={tvoc}, CO2={co2}")

            # Wait for a specified interval before the next read (e.g., 10 seconds)
            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Start the sensor monitoring in a separate thread
    sensor_thread = threading.Thread(target=monitor_sensors, daemon=True)
    sensor_thread.start()

    # Start the Flask REST API
    app.run(debug=True, host="0.0.0.0")
