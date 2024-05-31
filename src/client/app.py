from client.components.table import Table
from reader import Reader


class App:
    def __init__(self, reader: Reader) -> None:
        self.rendered_components = {}
        self.measurements = {}
        self.reader = reader
        self.reader.clear_measurements()

    def get_measurements(self) -> None:
        board_temperature, sensor_temperature, sensor_humidity, *_ = (
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

        self.measurements["board_temperature"] = board_temperature
        self.measurements["sensor_temperature"] = sensor_temperature
        self.measurements["sensor_humidity"] = sensor_humidity
        self.measurements["temperature_headers"] = temperature_headers
        self.measurements["temperature_records"] = temperature_records
        self.measurements["humidity_headers"] = humidity_headers
        self.measurements["humidity_records"] = humidity_records

    def set_page(self, page: str) -> None:
        if page == "table":
            self.rendered_components = {
                "temperature_table": Table(
                    self.measurements["temperature_headers"],
                    self.measurements["temperature_records"],
                    "°C",
                ),
                "humidity_table": Table(
                    self.measurements["humidity_headers"],
                    self.measurements["humidity_records"],
                    "%",
                ),
            }

    def render(self, page: str) -> str:
        self.get_measurements()
        self.set_page(page)
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Pico W</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" />
            </head>
            <body>
                <header class="container">
                    <h1>Pico W Dashboard</h1>
                </header>
                <nav class="container">
                  <ul>
                    <li><strong>Acme Corp</strong></li>
                  </ul>
                  <ul>
                    <li><a href="#" class="contrast">Table</a></li>
                    <li><a href="/chart" class="contrast">Chart</a></li>
                    <li><a href="/options" class="contrast">Options</a></li>
                  </ul>
                </nav>
                <div class="container">
                    <div class="grid">
                        <article>
                            <h2>Temperature</h2>
                            <hr>
                            <b>DHT11:</b> {self.measurements["sensor_temperature"]}°C
                            <br>
                            <b>internal sensor:</b> {self.measurements["board_temperature"]}°C
                            <hr>
                            <h3>History</h3>
                            {self.rendered_components["temperature_table"].generate_template()}
                        </article>
                        <article>
                            <h2>Humidity</h2>
                            <hr>
                            <b>DHT11:</b> {self.measurements["sensor_humidity"]}%
                            <br><br>
                            <hr>
                            <h3>History</h3>
                            {self.rendered_components["humidity_table"].generate_template()}
                        </article>
                    </div>
                </div>
            </body>
            </html>
        """

    def generate_options_template(self):
        return """<table>
  <thead>
    <tr>
      <th scope="col">Planet</th>
      <th scope="col">Diameter (km)</th>
      <th scope="col">Distance to Sun (AU)</th>
      <th scope="col">Orbit (days)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Mercury</th>
      <td>4,880</td>
      <td>0.39</td>
      <td>88</td>
    </tr>
    <tr>
      <th scope="row">Venus</th>
      <td>12,104</td>
      <td>0.72</td>
      <td>225</td>
    </tr>
    <tr>
      <th scope="row">Earth</th>
      <td>12,742</td>
      <td>1.00</td>
      <td>365</td>
    </tr>
    <tr>
      <th scope="row">Mars</th>
      <td>6,779</td>
      <td>1.52</td>
      <td>687</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Average</th>
      <td>9,126</td>
      <td>0.91</td>
      <td>341</td>
    </tr>
  </tfoot>
</table>"""
