from client.app import App
from client.components.options import Options
from client.components.table import Table
from client.components.table_container import TableContainer
from reader import Reader


class UIManager:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader
        self.temperature_headers = ["internal", "DHT11", "BMP280"]
        self.humidity_headers = ["DHT11"]
        self.pressure_headers = ["BMP280"]
        self.temperature_units = "°C"
        self.humidity_units = "%"
        self.pressure_units = "hPa"

    def get_app_template(self, page: str):
        if page == "tables":
            page_template = self.get_table_container_template()
        elif page == "options":
            page_template = self.get_options_template()
        else:
            page_template = ""
        return App(page_template).render()

    def get_table_template(self, table_type: str):
        # TODO: split into 3 txt files so we don't read all of these at once
        records = self.reader.read_saved_measurements_by_category(
            category=table_type, top=5
        )
        if table_type == "temperature":
            return Table(
                ["internal", "DHT11", "BMP280"],
                records,
                "°C",
            ).render()
        if table_type == "humidity":
            return Table(
                ["DHT11"],
                records,
                "%",
            ).render()
        if table_type == "pressure":
            return Table(
                ["BMP280"],
                records,
                "hPa",
            ).render()
        return ""

    def get_table_container_template(self):
        current_measurements = self.reader.read_measurements()

        return TableContainer(
            current_measurements,
            self.get_table_template("temperature"),
            self.get_table_template("humidity"),
            self.get_table_template("pressure"),
        ).render()

    def get_options_template(self):
        return Options().render()

    def get_chart_data(self, category: str):
        return self.reader.read_saved_measurements_by_category(category)
