import time

import network

from reader import Reader
from templates.dashboard import DashboardView


class Server:
    def __init__(
        self,
        reader: Reader,
        dashboard_view: DashboardView,
    ) -> None:
        self.server_socket = None
        self.reader = reader
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
            print("Waiting for connection...")
            time.sleep(1)
        if wlan.status() != 3:
            raise RuntimeError("Network connection failed")
        else:
            print("Connected to network")
            status = wlan.ifconfig()
            print("IP = " + status[0])

    async def async_handle_connections(self, reader, writer) -> None:
        print("Client connected")

        while await reader.readline() != b"\r\n":
            pass

        pico_temperature, sensor_temperature, sensor_humidity, *_ = (
            self.reader.read_measurements()
        )

        temperature_headers = ["internal", "DHT11"]
        humidity_headers = ["DHT11"]

        temperature_records = []
        humidity_records = []

        records = self.reader.read_saved_measurements(top=5)
        for record in records:
            temperature_records.append(record[:2])
            humidity_records.append(record[-1:])

        response = self.dashboard_view.generate_template(
            board_temperature=pico_temperature,
            sensor_temperature=sensor_temperature,
            sensor_humidity=sensor_humidity,
            temperature_headers=temperature_headers,
            temperature_records=temperature_records,
            humidity_headers=humidity_headers,
            humidity_records=humidity_records,
        )

        writer.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()
        print("Client Disconnected")
