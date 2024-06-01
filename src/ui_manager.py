from client.app import App
from client.components.options import Options
from client.components.table import Table
from client.components.table_container import TableContainer
from reader import Reader


class UIManager:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader

    def get_app_template(self, page: str):
        if page == "table":
            page_template = self.get_table_container_template()
        elif page == "options":
            page_template = self.get_options_template()
        else:
            page_template = ""
        return App(page_template).render()

    def get_table_template(
        self, headers: list[str], records: list[list[str]], unit: str
    ):
        return Table(headers, records, unit).render()

    def get_table_container_template(self):
        temperature_records, humidity_records, pressure_records = (
            self.reader.read_saved_measurements_by_category(top=5)
        )
        current_measurements = self.reader.read_measurements()
        temperature_table_template = Table(
            ["internal", "DHT11", "BMP280"],
            temperature_records,
            "°C",
        ).render()
        humidity_table_template = Table(
            ["DHT11"],
            humidity_records,
            "%",
        ).render()
        pressure_table_template = Table(
            ["BMP280"],
            pressure_records,
            "hPa",
        ).render()
        return TableContainer(
            current_measurements,
            temperature_table_template,
            humidity_table_template,
            pressure_table_template,
        ).render()

    def get_options_template(self):
        return Options().render()
