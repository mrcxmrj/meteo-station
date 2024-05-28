from client.app import App
from reader import Reader


class Router:
    def __init__(self, reader: Reader) -> None:
        self.server_socket = None
        self.reader = reader
        self.app = App()

    def route(self, method: str, route: str):
        print(f"Routing: {method}{route}")
        if route == "/":
            if method == "GET":
                return self.get_index()
        if route == "/options":
            if method == "GET":
                return self.get_options()
        elif route == "/clear-db":
            if method == "POST":
                print("POST /clear-db")
        else:
            print("Routing error: no route matched")

    def get_index(self):
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

        return self.app.generate_template(
            board_temperature=pico_temperature,
            sensor_temperature=sensor_temperature,
            sensor_humidity=sensor_humidity,
            temperature_headers=temperature_headers,
            temperature_records=temperature_records,
            humidity_headers=humidity_headers,
            humidity_records=humidity_records,
        )

    def get_options(self):
        return self.app.generate_options_template()
