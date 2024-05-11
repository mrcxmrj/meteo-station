from config import WIFI_PASSWORD, WIFI_SSID
from controllers.dht11 import DHT11
from controllers.pico import Pico
from server import Server
from views.dashboard import DashboardView

ssid = WIFI_SSID
password = WIFI_PASSWORD

server = Server(
    board=Pico(), humidity_temperature_sensor=DHT11(28), dashboard_view=DashboardView()
)
server.connect(ssid, password)
server.listen("0.0.0.0", 80)
server.handle_connections()
