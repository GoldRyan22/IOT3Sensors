from flask import Flask, render_template, send_file
from io import BytesIO
import matplotlib.pyplot as plt
import pyrebase
from datetime import datetime
# import pyrebase and use the Firebase-fetching code you already wrote
config = {
    "apiKey": "AIzaSyA_ikc_5_3gPEmBpm9XCvn2l6vAnbALGoc",
    "authDomain": "iot-3sensors.firebaseapp.com",
    "databaseURL": "https://iot-3sensors-default-rtdb.firebaseio.com",
    "storageBucket": "iot-3sensors.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)



def fetch_temperatures(sensor_key):
    data = db.child(sensor_key).get()
    temps = []
    keys = []

    if data.each() is not None:
        for entry in data.each():
            val = entry.val()
            if 'Temperature' in val:
                temps.append(val['Temperature'])
                keys.append(entry.key())  # Use push ID as timestamp (or replace with actual timestamp)
    return keys, temps


# Fetch data
#timestamps1, temps1 = fetch_temperatures("Status1")
#timestamps2, temps2 = fetch_temperatures("Status2")
#timestamps3, temps3 = fetch_temperatures("Status3")

def get_all_data():
    timestamps1, temps1 = fetch_temperatures("Status1")
    timestamps2, temps2 = fetch_temperatures("Status2")
    timestamps3, temps3 = fetch_temperatures("Status3")

    length = min(len(temps1), len(temps2), len(temps3))
    if length == 0:
        return [], [], [], [], []

    temps1 = temps1[:length]
    temps2 = temps2[:length]
    temps3 = temps3[:length]
    timestamps = list(range(1, length + 1))

    valid1, valid2, valid3 = True, True, True   
    averages = []

    for i in range(length):
        readings = []
        if valid1:
            readings.append(temps1[i])
        if valid2:
            readings.append(temps2[i])
        if valid3:
            readings.append(temps3[i])

        if not readings:
            averages.append(0)
            continue

        avg = sum(readings) / len(readings)
        averages.append(round(avg, 2))
        
        vin1, vin2, vin3 = len(temps1), len(temps2), len(temps3)

        # Check for rogue sensor
        if valid1 and abs(temps1[i] - temps2[i]) > 10 and abs(temps1[i] - temps3[i]) > 10:
            print(f"❌ Sensor1 went rogue at index {i}, excluding it.")
            valid1 = False
            vin1 = i
        if valid2 and abs(temps2[i] - temps1[i]) > 10 and abs(temps2[i] - temps3[i]) > 10:
            print(f"❌ Sensor2 went rogue at index {i}, excluding it.")
            valid2 = False
            vin2 = i
        if valid3 and abs(temps3[i] - temps2[i]) > 10 and abs(temps3[i] - temps1[i]) > 10:
            print(f"❌ Sensor3 went rogue at index {i}, excluding it.")
            valid3 = False
            vin3 = i

    # Filter out invalid sensors
    #temps1 = temps1 if valid1 else [None] * length
    #temps2 = temps2 if valid2 else [None] * length
    #temps3 = temps3 if valid3 else [None] * length
    
    
    if vin1 < len(temps1) :
        temps1[vin1:] = [None] * (len(temps1) - vin1) 
        
    
    if vin2 < len(temps2) :
        temps2[vin2:] = [None] * (len(temps2) - vin2) 
           
    
    if vin3 < len(temps3) :
        temps3[vin3:] = [None] * (len(temps3) - vin3)
    return timestamps, temps1, temps2, temps3, averages

def plot_sensor_data(timestamps, temps1, temps2, temps3, averages):
    fig = plt.figure(figsize=(14, 8))

    # Sensor 1
    plt.subplot(4, 1, 1)
    plt.plot(timestamps, temps1, marker='o', color='red')
    plt.title("Sensor 1 Temperature")
    plt.ylabel("°C")
    plt.xticks(rotation=45)

    # Sensor 2
    plt.subplot(4, 1, 2)
    plt.plot(timestamps, temps2, marker='o', color='blue')
    plt.title("Sensor 2 Temperature")
    plt.ylabel("°C")
    plt.xticks(rotation=45)

    # Sensor 3
    plt.subplot(4, 1, 3)
    plt.plot(timestamps, temps3, marker='o', color='green')
    plt.title("Sensor 3 Temperature")
    plt.ylabel("°C")
    plt.xticks(rotation=45)

    # Average
    plt.subplot(4, 1, 4)
    plt.plot(timestamps, averages, marker='o', color='purple')
    plt.title("Average Temperature Across Sensors")
    plt.xlabel("Timestamp")
    plt.ylabel("°C")
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig  # Return the figure object, don't call plt.show()


@app.route('/')
def index():
    # Generate your matplotlib figure here
    timestamps, temps1, temps2, temps3, averages = get_all_data()
    fig = plot_sensor_data(timestamps, temps1, temps2, temps3, averages)  # Replace with your plotting function
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
