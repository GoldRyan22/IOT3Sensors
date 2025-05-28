import pyrebase
import matplotlib.pyplot as plt

# Firebase config
config = {
    "apiKey": "AIzaSyA_ikc_5_3gPEmBpm9XCvn2l6vAnbALGoc",
    "authDomain": "iot-3sensors.firebaseapp.com",
    "databaseURL": "https://iot-3sensors-default-rtdb.firebaseio.com",
    "storageBucket": "iot-3sensors.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def fetch_temperatures(sensor_key):
    # Get all data under the sensor key
    data = db.child(sensor_key).get()
    temperatures = []
    timestamps = []
    
    count = 0

    if data.each() is not None:
        for entry in data.each():
            value = entry.val()
            if 'Temperature' in value:
                temperatures.append(value['Temperature'])
                # Optionally use entry.key() as a pseudo timestamp
                timestamps.append(entry.key())
    return timestamps, temperatures

# Fetch data for each sensor
timestamps1, temps1 = fetch_temperatures("Status1")
timestamps2, temps2 = fetch_temperatures("Status2")
timestamps3, temps3 = fetch_temperatures("Status3")

# Plotting
plt.figure(figsize=(12, 6))

# Sensor 1
plt.subplot(3, 1, 1)
plt.plot(timestamps1, temps1, marker='o', label='Sensor 1', color='red')
plt.title("Temperature Readings from Sensor 1")
plt.ylabel("Temp (°C)")
plt.xticks(rotation=45)

# Sensor 2
plt.subplot(3, 1, 2)
plt.plot(timestamps2, temps2, marker='o', label='Sensor 2', color='blue')
plt.title("Temperature Readings from Sensor 2")
plt.ylabel("Temp (°C)")
plt.xticks(rotation=45)

# Sensor 3
plt.subplot(3, 1, 3)
plt.plot(timestamps3, temps3, marker='o', label='Sensor 3', color='green')
plt.title("Temperature Readings from Sensor 3")
plt.xlabel("Entry ID (or Timestamp)")
plt.ylabel("Temp (°C)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
