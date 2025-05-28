import time
import board
import pyrebase
import adafruit_dht

config = {
    "apiKey": "AIzaSyA_ikc_5_3gPEmBpm9XCvn2l6vAnbALGoc",
    "authDomain": "iot-3sensors.firebaseapp.com",
    "databaseURL": "https://iot-3sensors-default-rtdb.firebaseio.com",
    "storageBucket": "iot-3sensors.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

dhtDevice1 = adafruit_dht.DHT11(board.D17, use_pulseio=False)
dhtDevice2 = adafruit_dht.DHT11(board.D27, use_pulseio=False)
dhtDevice3 = adafruit_dht.DHT11(board.D22, use_pulseio=False)

while True:
    try:
        temperature_c1 = dhtDevice1.temperature
        temperature_c2 = dhtDevice2.temperature
        temperature_c3 = dhtDevice3.temperature

        print(
            "Temp: {:.1f} C {:.1f} C {:.1f} C".format(
                temperature_c1, temperature_c2, temperature_c3
            )
        )

        data1 = {
            "Temperature": temperature_c1
        }

        data2 = {
            "Temperature": temperature_c2
        }

        data3 = {
            "Temperature": temperature_c3
        }

        db.child("Status1").push(data1)
        db.update(data1)

        db.child("Status2").push(data2)
        db.update(data2)

        db.child("Status3").push(data3)
        db.update(data3)

        print("Sent to firebase")

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        dhtDevice1.exit()
        dhtDevice2.exit()
        dhtDevice3.exit()
        raise error

    time.sleep(2.0)
