import asyncio

from client.app import App
from config import WIFI_PASSWORD, WIFI_SSID
from reader import Reader
from router import Router
from sensors.dht11 import DHT11
from sensors.pico import Pico
from server import Server

ssid = WIFI_SSID
password = WIFI_PASSWORD

reader = Reader(
    board=Pico(), humidity_temperature_sensor=DHT11(28), output_path="output.txt"
)
reader.clear_measurements()

app_ui = App(reader=reader)

router = Router(app_ui=app_ui)

server = Server(router=router)
server.connect(ssid, password)


async def main():
    async_server = asyncio.start_server(server.async_handle_connections, "0.0.0.0", 80)
    read_loop = reader.read_loop(3)
    asyncio.create_task(async_server)
    asyncio.create_task(read_loop)


loop = asyncio.get_event_loop()
loop.create_task(main())

try:
    loop.run_forever()
except Exception as e:
    print("Error occured: ", e)
except KeyboardInterrupt:
    print("Program interrupted")
