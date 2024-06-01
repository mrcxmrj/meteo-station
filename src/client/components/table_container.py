from client.components.table import Table
from reader import Reader


class TableContainer:
    def __init__(
        self,
        reader: Reader,
    ) -> None:
        self.reader = reader
        self.temperature_table, self.humidity_table, self.pressure_table = (
            self.create_data_tables()
        )

    def create_data_tables(self) -> tuple[Table, Table, Table]:
        temperature_headers = ["internal", "DHT11", "BMP280"]
        humidity_headers = ["DHT11"]
        pressure_headers = ["BMP280"]

        temperature_records = []
        humidity_records = []
        pressure_records = []

        records = self.reader.read_saved_measurements(top=5)
        for record in records:
            temperature_records.append([record[0], record[2], record[4]])
            humidity_records.append([record[1]])
            pressure_records.append([record[3]])

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
        pressure_table = Table(
            pressure_headers,
            pressure_records,
            "hPa",
        )
        return temperature_table, humidity_table, pressure_table

    def render(self) -> str:
        (
            current_board_temperature,
            current_dht_humidity,
            current_dht_temperature,
            current_bmp_pressure,
            current_bmp_temperature,
        ) = self.reader.read_measurements()
        return f"""
            <div class="grid">
                <article>
                    <h2>Temperature</h2>
                    <hr>
                    <b>internal sensor:</b> {current_board_temperature}°C
                    <br>
                    <b>DHT11:</b> {current_dht_temperature}°C
                    <br>
                    <b>BMP280:</b> {current_bmp_temperature}°C
                    <hr>
                    <h3>History</h3>
                    {self.temperature_table.render()}
                </article>
                <article>
                    <h2>Humidity</h2>
                    <hr>
                    <b>DHT11:</b> {current_dht_humidity}%
                    <br><br><br>
                    <hr>
                    <h3>History</h3>
                    {self.humidity_table.render()}
                </article>
                <article>
                    <h2>Pressure</h2>
                    <hr>
                    <b>BMP280:</b> {current_bmp_pressure}hPa
                    <br><br><br>
                    <hr>
                    <h3>History</h3>
                    {self.pressure_table.render()}
                </article>
            </div>
        """
