import time

import network

from router import Router


class Server:
    def __init__(
        self,
        router: Router,
    ) -> None:
        self.server_socket = None
        self.router = router

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

        request_line = await reader.readline()
        method, route, *_ = request_line.decode("utf-8").split()
        status_code, reason_phrase, content_type, body = self.router.route(
            method, route
        )

        # skip request headers
        while await reader.readline() != b"\r\n":
            pass

        writer.write(
            f"HTTP/1.0 {status_code} {reason_phrase}\r\nContent-type: {content_type}\r\n\r\n"
        )
        if body:
            writer.write(body)

        await writer.drain()
        await writer.wait_closed()
        print("Client Disconnected")
