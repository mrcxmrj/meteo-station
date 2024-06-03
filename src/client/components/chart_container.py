import json


class ChartContainer:
    def __init__(self, records: list[dict[str, str | list[str]]]) -> None:
        self.records = records

    def render(self):
        return f"""
            <div class="container">
                <article>
                    <div id="chart">
                    </div>
                </article>
            </div>
            <script src="https://unpkg.com/lightweight-charts@4.1.4/dist/lightweight-charts.standalone.production.js"></script>
            <script>
                const initialData = {json.dumps(self.records)}
            </script>
            <script src="js/chart.js"></script>
        """
