import json


class Chart:
    def __init__(
        self, records: list[dict[str, str | list[str]]], category: str
    ) -> None:
        self.records = records
        self.category = category

    def get_unit(self):
        if self.category == "temperature":
            return "°C"
        elif self.category == "humidity":
            return "%"
        else:
            return "hPa"

    def render(self):
        return f"""
            <div id="chart">
            </div>
            <script>
                const initialData = {json.dumps(self.records)}
                const category = "{self.category}"
                const unit = "{self.get_unit()}";
            </script>
            <script src="js/chart.js"></script>
        """
