import asyncio

from config import WIFI_PASSWORD, WIFI_SSID
from sensors.dht11 import DHT11
from sensors.pico import Pico
from server import Server
from templates.dashboard import DashboardView

ssid = WIFI_SSID
password = WIFI_PASSWORD

server = Server(
    board=Pico(), humidity_temperature_sensor=DHT11(28), dashboard_view=DashboardView()
)
server.connect(ssid, password)
# server.listen("0.0.0.0", 80)


async def main():
    async_server = asyncio.start_server(server.async_handle_connections, "0.0.0.0", 80)
    asyncio.create_task(async_server)
    while True:
        await asyncio.sleep(5)
        print("This message will be printed every 5 seconds")


loop = asyncio.get_event_loop()
loop.create_task(main())

try:
    loop.run_forever()
except Exception as e:
    print("Error occured: ", e)
except KeyboardInterrupt:
    print("Program interrupted")
