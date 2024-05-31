from client.components.options import Options
from client.components.table import Table
from reader import Reader


class App:
    def __init__(self, reader: Reader) -> None:
        self.rendered_components = {}
        self.reader = reader
        self.reader.clear_measurements()

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

    def set_page(self, page: str) -> None:
        if page == "table":
            temperature_table, humidity_table = self.create_data_tables()
            self.rendered_components = {
                "temperature_table": temperature_table,
                "humidity_table": humidity_table,
            }
        elif page == "options":
            self.rendered_components = {"options": Options()}

    def render(self, page: str) -> str:
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
                            {self.rendered_components["temperature_table"].render()}
                        </article>
                        <article>
                            <h2>Humidity</h2>
                            <hr>
                            {self.rendered_components["humidity_table"].render()}
                        </article>
                    </div>
                </div>
            </body>
            </html>
        """
