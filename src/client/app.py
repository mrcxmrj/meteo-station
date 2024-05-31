from client.components.options import Options
from client.components.table_container import TableContainer
from reader import Reader


class App:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader
        self.page: TableContainer | Options | None = None

    def set_page(self, page: str) -> None:
        if page == "table":
            self.page = TableContainer(self.reader)
        elif page == "options":
            self.page = Options()
        else:
            self.page = None

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
                    <li><a href="/table" class="contrast">Table</a></li>
                    <li><a href="/chart" class="contrast">Chart</a></li>
                    <li><a href="/options" class="contrast">Options</a></li>
                  </ul>
                </nav>
                <div class="container">
                    { self.page.render()if self.page is not None else ""}
                </div>
                <script src="js/script.js" ></script>
            </body>
            </html>
        """
