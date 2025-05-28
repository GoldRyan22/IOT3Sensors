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
timestamps1, temps1 = fetch_temperatures("Status1")
timestamps2, temps2 = fetch_temperatures("Status2")
timestamps3, temps3 = fetch_temperatures("Status3")

# Ensure same length (assumes aligned order)
length = min(len(temps1), len(temps2), len(temps3))
timestamps = timestamps1[:length]
temps1 = temps1[:length]
temps2 = temps2[:length]
temps3 = temps3[:length]

# Compute averages and check for outliers
averages = []
for i in range(length):
    t1 = temps1[i]
    t2 = temps2[i]
    t3 = temps3[i]
    avg = round((t1 + t2 + t3) / 3, 2)
    averages.append(avg)

    # Outlier detection
    for sensor, temp in zip(["Sensor1", "Sensor2", "Sensor3"], [t1, t2, t3]):
        if abs(temp - avg) > 3:
            print(f"⚠️  Outlier at {timestamps[i]} - {sensor} is off by {abs(temp - avg):.2f}°C (Temp: {temp}, Avg: {avg})")

# Plotting
plt.figure(figsize=(14, 8))

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
plt.show()
