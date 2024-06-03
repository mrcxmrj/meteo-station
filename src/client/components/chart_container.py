class ChartContainer:
    def __init__(self) -> None:
        pass

    def render(self):
        return """
            <div class="container">
                <article>
                    <div id="chart">
                    </div>
                </article>
            </div>
            <script src="https://unpkg.com/lightweight-charts@4.1.4/dist/lightweight-charts.standalone.production.js"></script>
            <script src="js/chart.js"></script>
        """
