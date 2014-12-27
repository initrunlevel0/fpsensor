import socket
import json
import time

port = 5000
host = '255.255.255.255'


# Define UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

while True:
    # Read from Socket
    dataOutside, addr = s.recvfrom(1024)
    dataOutside = json.loads(dataOutside)
    print "Received dataOutside, " + str(dataOutside)
    time.sleep(5)



