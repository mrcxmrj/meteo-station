import json


class ChartContainer:
    def __init__(
        self, records: list[dict[str, str | list[str]]], category: str
    ) -> None:
        self.records = records
        self.category = category

    def render(self):
        return f"""
            <div class="container">
                <h2>{self.category}</h2>
                <article>
                    <div id="chart">
                    </div>
                </article>
            </div>
            <script src="https://unpkg.com/lightweight-charts@4.1.4/dist/lightweight-charts.standalone.production.js"></script>
            <script>
                const initialData = {json.dumps(self.records)}
                const category = "{self.category}"
            </script>
            <script src="js/chart.js"></script>
        """
