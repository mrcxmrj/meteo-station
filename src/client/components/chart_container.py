class ChartContainer:
    def __init__(self, chart_template: str, selected_category: str = "") -> None:
        self.chart_template = chart_template
        self.selected_category = selected_category
        self.dropdown_items = {
            "temperature": '<li><a href="/charts/temperature" class="chart-option" data-id="temperature">temperature</a></li>',
            "humidity": '<li><a href="/charts/humidity" class="chart-option" data-id="humidity">humidity</a></li>',
            "pressure": '<li><a href="/charts/pressure" class="chart-option" data-id="pressure">pressure</a></li>',
        }
        if selected_category != "":
            del self.dropdown_items[selected_category]

    def render(self):
        return f"""
            <script src="https://unpkg.com/lightweight-charts@4.1.4/dist/lightweight-charts.standalone.production.js"></script>
            <div class="container" id="chart-container">
                <details class="dropdown">
                    <summary>{ self.selected_category if self.selected_category != "" else "select category" }</summary>
                    <ul>
                        {"".join(self.dropdown_items.values())}
                    </ul>
                </details>
                <article>
                    {self.chart_template}
                </article>
            </div>
        """
