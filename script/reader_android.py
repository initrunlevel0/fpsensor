# Using Adafruit_Python_DHT library to read DHT sensor
# https://github.com/adafruit/Adafruit_Python_DHT

import socket
import json
import time
import threading
import androidhelper

droid = androidhelper.Android()

port = 5000

# First, ask about broadcast address
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

            if dataOutside['source'] != "android":
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
            # Read Android Sensor
            droid.startSensingTimed(4,250)
            light = droid.sensorsGetLight().result
            if(light is not None):
                # Create a dictionary data to send to socket
                dataInside['light'] = light
                dataInside['source'] = "android"

                # Send to socket
                s.sendto(json.dumps(dataInside), (host, port))
                print "Set dataInside, " + str(dataInside)

                # Send also into REST API
                # TODO

        except:
            pass



t1 = threading.Thread(target=readFromOutside, args=())
t1.start()
t2 = threading.Thread(target=readInside, args=())
t2.start()
