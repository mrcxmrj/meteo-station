import json


class Chart:
    def __init__(
        self, records: list[dict[str, str | list[str]]], category: str
    ) -> None:
        self.records = records
        self.category = category

    def render(self):
        return f"""
            <div id="chart">
            </div>
            <script>
                const initialData = {json.dumps(self.records)}
                const category = "{self.category}"
            </script>
            <script src="js/chart.js"></script>
        """
