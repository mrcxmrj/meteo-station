from client.components.table import Table


class App:
    def __init__(self) -> None:
        self.rendered_components = {}

    def generate_template(
        self,
        page: str,
        board_temperature: float,
        sensor_temperature: float,
        sensor_humidity: float,
        temperature_headers: list[str],
        temperature_records: list[list[str]],
        humidity_headers: list[str],
        humidity_records: list[list[str]],
    ) -> str:
        if page == "table":
            self.rendered_components = {
                "temperature_table": Table(
                    temperature_headers, temperature_records, "°C"
                ),
                "humidity_table": Table(humidity_headers, humidity_records, "%"),
            }

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
                            <b>DHT11:</b> {sensor_temperature}°C
                            <br>
                            <b>internal sensor:</b> {board_temperature}°C
                            <hr>
                            <h3>History</h3>
                            {self.rendered_components["temperature_table"].generate_template()}
                        </article>
                        <article>
                            <h2>Humidity</h2>
                            <hr>
                            <b>DHT11:</b> {sensor_humidity}%
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
