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
            print("waiting for connection...")
            time.sleep(1)
        if wlan.status() != 3:
            raise RuntimeError("network connection failed")
        else:
            print("connected")
            status = wlan.ifconfig()
            print("ip = " + status[0])

    async def async_handle_connections(self, reader, writer) -> None:
        print("Client connected")

        while await reader.readline() != b"\r\n":
            pass

        pico_temperature, sensor_temperature, sensor_humidity, *_ = (
            self.reader.read_measurements()
        )

        headers = ["Board", "DHT11"]
        records = [[str(pico_temperature), str(sensor_temperature)] for _ in range(10)]

        response = self.dashboard_view.generate_template(
            pico_temperature,
            sensor_temperature,
            sensor_humidity,
            headers,
            records,
            headers,
            records,
        )

        writer.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()
        print("Client Disconnected")
