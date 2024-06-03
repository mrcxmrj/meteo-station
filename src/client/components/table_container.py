class TableContainer:
    def __init__(
        self,
        current_measurements: tuple[float, float, float, float, float],
        temperature_table_template: str,
        humidity_table_template: str,
        pressure_table_template: str,
    ) -> None:
        self.current_measurements = current_measurements
        self.temperature_table_template = temperature_table_template
        self.humidity_table_template = humidity_table_template
        self.pressure_table_template = pressure_table_template

    def render(self) -> str:
        (
            current_board_temperature,
            current_dht_humidity,
            current_dht_temperature,
            current_bmp_pressure,
            current_bmp_temperature,
        ) = self.current_measurements
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
                    <div id="temperature-table">
                    {self.temperature_table_template}
                    </div>
                </article>
                <article>
                    <h2>Humidity</h2>
                    <hr>
                    <b>DHT11:</b> {current_dht_humidity}%
                    <br><br><br>
                    <hr>
                    <h3>History</h3>
                    <div id="humidity-table">
                    {self.humidity_table_template}
                    </div>
                </article>
                <article>
                    <h2>Pressure</h2>
                    <hr>
                    <b>BMP280:</b> {current_bmp_pressure}hPa
                    <br><br><br>
                    <hr>
                    <h3>History</h3>
                    <div id="pressure-table">
                    {self.pressure_table_template}
                    </div>
                </article>
            </div>
            <script src="js/tables.js" ></script>
        """
