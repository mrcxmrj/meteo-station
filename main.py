import socket
import time

import network

from config import WIFI_PASSWORD, WIFI_SSID
from controllers import pico

ssid = WIFI_SSID
password = WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """
<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W</h1>
<p>Hello World</p>
</body>
</html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print("ip = " + status[0])

# Open socket
server_address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server_socket = socket.socket()
server_socket.bind(server_address)
server_socket.listen(1)

print("listening on", server_address)

client_socket = None
# Listen for connections
while True:
    try:
        client_socket, remote_address = server_socket.accept()
        print("client connected from", remote_address)
        pico.blink_led()
        cl_file = client_socket.makefile("rwb", 0)
        while True:
            line = cl_file.readline()
            if not line or line == b"\r\n":
                break
        response = html
        client_socket.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        client_socket.send(response)
        client_socket.close()

    except OSError as e:
        if client_socket:
            client_socket.close()
        print("connection closed")
