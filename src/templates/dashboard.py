class DashboardView:
    def generate_template(
        self,
        board_temperature: float,
        sensor_temperature: float,
        sensor_humidity: float,
    ) -> str:
        board_temperature = round(board_temperature, 2)
        sensor_temperature = round(sensor_temperature, 2)
        sensor_humidity = round(sensor_humidity, 2)
        headers = ["Board", "DHT11"]
        records = [[str(board_temperature), str(sensor_temperature)] for _ in range(10)]

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
                            {self.generate_table(headers, records)}
                        </article>
                        <article>
                            <h2>Humidity</h2>
                            <hr>
                            <b>DHT11:</b> {sensor_humidity}%
                        </article>
                    </div>
                </div>
            </body>
            </html>
        """

    def generate_table(self, headers: list[str], records: list[list[str]]) -> str:
        headers_html: str = (
            "<tr>"
            + '<th scope="col"></th>'
            + "".join([f'<th scope="col">{header}</th>' for header in headers])
            + "</tr>"
        )
        records_html: list[str] = [
            "".join([f"<td>{value}</td>" for value in record]) for record in records
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
        averages = [sum / len(records) for sum in sums]
        footer_html: str = (
            "<tr>"
            + '<th scope="row">Average</th>'
            + "".join([f"<td>{average}</td>" for average in averages])
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
