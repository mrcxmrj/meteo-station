from client.components.table import Table
from reader import Reader


class TableContainer:
    def __init__(
        self,
        reader: Reader,
    ) -> None:
        self.reader = reader
        self.temperature_table, self.humidity_table = self.create_data_tables()

    def create_data_tables(self) -> tuple[Table, Table]:
        temperature_headers = ["internal", "DHT11"]
        humidity_headers = ["DHT11"]

        temperature_records = []
        humidity_records = []

        records = self.reader.read_saved_measurements(top=5)
        for record in records:
            temperature_records.append(record[:2])
            humidity_records.append(record[-1:])

        temperature_table = Table(
            temperature_headers,
            temperature_records,
            "°C",
        )
        humidity_table = Table(
            humidity_headers,
            humidity_records,
            "%",
        )
        return temperature_table, humidity_table

    def render(self) -> str:
        current_board_temperature, current_temperature, current_humidity, *_ = (
            self.reader.read_measurements()
        )
        return f"""
            <div class="grid">
                <article>
                    <h2>Temperature</h2>
                    <hr>
                    <b>DHT11:</b> {current_temperature}°C
                    <br>
                    <b>internal sensor:</b> {current_board_temperature}°C
                    <hr>
                    <h3>History</h3>
                    <hr>
                    {self.temperature_table.render()}
                </article>
                <article>
                    <h2>Humidity</h2>
                    <hr>
                    <b>DHT11:</b> {current_humidity}%
                    <br><br>
                    <hr>
                    <h3>History</h3>
                    <hr>
                    {self.humidity_table.render()}
                </article>
            </div>
        """
