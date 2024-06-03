class ChartContainer:
    def __init__(self, chart_template: str) -> None:
        self.chart_template = chart_template

    def render(self):
        return f"""
            <script src="https://unpkg.com/lightweight-charts@4.1.4/dist/lightweight-charts.standalone.production.js"></script>
            <div class="container">
                <article>
                    {self.chart_template}
                </article>
            </div>
        """
