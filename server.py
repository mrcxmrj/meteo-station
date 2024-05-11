import socket
import time

import network

from controllers.dht11 import DHT11
from controllers.pico import Pico
from views.dashboard import DashboardView


class Server:
    def __init__(
        self,
        board: Pico,
        humidity_temperature_sensor: DHT11,
        dashboard_view: DashboardView,
    ) -> None:
        self.server_socket = None
        self.board = board
        self.humidity_temperature_sensor = humidity_temperature_sensor
        self.dashboard_view = dashboard_view

    def connect(
        self,
        ssid: str,
        password: str,
    ) -> None:
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

    def listen(self, address: str, port: int) -> None:
        server_address = socket.getaddrinfo(address, port)[0][-1]

        self.server_socket = socket.socket()
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)
        print("listening on", server_address)

    async def async_handle_connections(self, reader, writer) -> None:
        print("Client connected")

        while await reader.readline() != b"\r\n":
            pass

        self.board.blink_led()
        pico_temperature = self.board.read_temperature()
        sensor_temperature = self.humidity_temperature_sensor.read_temperature()
        sensor_humidity = self.humidity_temperature_sensor.read_humidity()

        response = self.dashboard_view.generate_template(
            pico_temperature, sensor_temperature, sensor_humidity
        )

        writer.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()
        print("Client Disconnected")

    def handle_connections(self) -> None:
        if not self.server_socket:
            print("server isn't listening")
            return

        while True:
            try:
                client_socket, remote_address = self.server_socket.accept()
                print("client connected from", remote_address)

                self.board.blink_led()
                pico_temperature = self.board.read_temperature()
                sensor_temperature = self.humidity_temperature_sensor.read_temperature()
                sensor_humidity = self.humidity_temperature_sensor.read_humidity()

                client_file = client_socket.makefile("rwb", 0)
                while True:
                    line = client_file.readline()
                    if not line or line == b"\r\n":
                        break

                response = self.dashboard_view.generate_template(
                    pico_temperature, sensor_temperature, sensor_humidity
                ).encode("utf-8")

                client_socket.send(
                    b"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
                )
                client_socket.send(response)
                client_socket.close()

            except OSError as e:
                print(e)
                if client_socket:
                    client_socket.close()
                print("connection closed")
