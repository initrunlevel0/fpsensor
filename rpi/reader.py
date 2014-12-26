# Using Adafruit_Python_DHT library to read DHT sensor
# https://github.com/adafruit/Adafruit_Python_DHT

import Adafruit_DHT
import socket
import json
import time
import thread

port = 5000
host = '255.255.255.255'


# Define UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

dataInside = {}
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
                # Create a dictionary data to send to socket
                dataInside['temperature'] = temperature
                dataInside['humidity'] = humidity
                dataInside['source'] = "raspi"
                print "Set dataInside, " + str(dataInside)

                # Send to socket
                s.sendto(json.dumps(dataInside), (host, port))

                # Send also into REST API
                # TODO

                time.sleep(5)
        except:
            pass



thread.start_new_thread(readFromOutside, ())
thread.start_new_thread(readInside, ())

