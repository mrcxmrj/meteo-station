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
        headers_html: str = '<th scope="col"></th>' + "".join(
            [f'<th scope="col">{header}</th>' for header in headers]
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

        return f"""
            <table class="striped">
                <thead>
                    <tr>
                        {headers_html}
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
                <tfoot>
                    <tr>
                        <th scope="row">Average</th>
                        <td>9,126</td>
                        <td>0.91</td>
                    </tr>
                </tfoot>
            </table>
        """
