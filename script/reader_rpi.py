# Using Adafruit_Python_DHT library to read DHT sensor
# https://github.com/adafruit/Adafruit_Python_DHT

import Adafruit_DHT
import socket
import json
import time
import threading

port = 5000
print "Masukkan alamat broadcast"
host = raw_input()


# Define UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

dataInside = {}
dataInside['temperature'] = 0
dataInside['humidity'] = 0
def readFromOutside():
    while True:
        try:
            # Read from Socket
            dataOutside, addr = s.recvfrom(1024)
            dataOutside = json.loads(dataOutside)

            if dataOutside['source'] != "raspi":
                print "Received dataOutside, " + str(dataOutside)

                # Save to my own data
                for key in dataOutside:
                    if key != "source":
                        dataInside[key] = dataOutside[key]
        except:
            pass

def readInside():
    while True:
        try:
            # Read DHT11 on pin 4, HARDCODED
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
            if(humidity is not None and temperature is not None):
                oldTemperature = dataInside['temperature']
                oldHumidity = dataInside['humidity']

                # Create a dictionary data to send to socket
                dataInside['temperature'] = temperature
                dataInside['humidity'] = humidity
                dataInside['source'] = "raspi"

                # Send to socket
                if oldHumidity != dataInside['humidity'] or oldTemperature != dataInside['temperature']:
                    s.sendto(json.dumps(dataInside), (host, port))
                    print "Set dataInside, " + str(dataInside)

                # Send also into REST API
                # TODO

                time.sleep(5)
        except:
            pass



t1 = threading.Thread(target=readFromOutside, args=())
t1.start()
t2 = threading.Thread(target=readInside, args=())
t2.start()
