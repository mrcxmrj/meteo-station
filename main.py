import socket
import time

import network

from config import WIFI_PASSWORD, WIFI_SSID
from controllers.dht11 import DHT11
from controllers.pico import Pico
from views.dashboard import DashboardView

ssid = WIFI_SSID
password = WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print("waiting for connection...")
    time.sleep(1)
if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print("ip = " + status[0])

server_address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server_socket = socket.socket()
server_socket.bind(server_address)
server_socket.listen(1)
client_socket = None
print("listening on", server_address)

humidity_temperature_sensor = DHT11(28)
board = Pico()

dashboard_view = DashboardView()

while True:
    try:
        client_socket, remote_address = server_socket.accept()
        print("client connected from", remote_address)

        board.blink_led()
        pico_temperature = board.read_temperature()
        sensor_temperature = humidity_temperature_sensor.read_temperature()
        sensor_humidity = humidity_temperature_sensor.read_humidity()

        client_file = client_socket.makefile("rwb", 0)
        while True:
            line = client_file.readline()
            if not line or line == b"\r\n":
                break

        response = dashboard_view.generate_template(
            pico_temperature, sensor_temperature, sensor_humidity
        ).encode("utf-8")

        client_socket.send(b"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        client_socket.send(response)
        client_socket.close()

    except OSError as e:
        print(e)
        if client_socket:
            client_socket.close()
        print("connection closed")
