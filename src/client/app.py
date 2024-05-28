class App:
    def generate_template(
        self,
        board_temperature: float,
        sensor_temperature: float,
        sensor_humidity: float,
        temperature_headers: list[str],
        temperature_records: list[list[str]],
        humidity_headers: list[str],
        humidity_records: list[list[str]],
    ) -> str:
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
                            {self.generate_table(temperature_headers, temperature_records, "°C")}
                        </article>
                        <article>
                            <h2>Humidity</h2>
                            <hr>
                            <b>DHT11:</b> {sensor_humidity}%
                            <br><br>
                            <hr>
                            <h3>History</h3>
                            {self.generate_table(humidity_headers, humidity_records, "%")}
                        </article>
                    </div>
                </div>
            </body>
            </html>
        """

    def generate_table(
        self, headers: list[str], records: list[list[str]], unit: str
    ) -> str:
        headers_html: str = (
            "<tr>"
            + '<th scope="col"></th>'
            + "".join([f'<th scope="col">{header}</th>' for header in headers])
            + "</tr>"
        )
        records_html: list[str] = [
            "".join([f"<td>{value}{unit}</td>" for value in record])
            for record in records
        ]

        rows_html = ""
        for index, row in enumerate(records_html):
            rows_html += "<tr>"
            rows_html += f'<th scope="row">{index}</th>'
            rows_html += row
            rows_html += "</tr>"

        sums = [0.0 for _ in headers]
        for record in records:
            for i, value in enumerate(record):
                sums[i] += float(value)
        averages = [round(sum / len(records), 2) for sum in sums]
        footer_html: str = (
            "<tr>"
            + '<th scope="row">Average</th>'
            + "".join([f"<td>{average}{unit}</td>" for average in averages])
            + "</tr>"
        )

        return f"""
            <table class="striped">
                <thead>
                    {headers_html}
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
                <tfoot>
                    {footer_html}
                </tfoot>
            </table>
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
