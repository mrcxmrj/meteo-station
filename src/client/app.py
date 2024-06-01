class App:
    def __init__(self, page_template: str) -> None:
        self.page_template = page_template

    def render(self) -> str:
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
                    <nav>
                        <ul>
                            <li><strong>Pico W Dashboard</strong></li>
                        </ul>
                        <ul>
                            <li><a href="/table" class="contrast">Table</a></li>
                            <li><a href="/chart" class="contrast">Chart</a></li>
                            <li><a href="/options" class="contrast">Options</a></li>
                        </ul>
                    </nav>
                </header>
                <div class="container">
                    {self.page_template}
                </div>
                <script src="js/script.js" ></script>
            </body>
            </html>
        """
