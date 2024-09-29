import json


class Thermometers:
    def __init__(self, records: list[dict[str, str | list[str]]], unit: str) -> None:
        self.records = records
        self.unit = unit

    def render(self) -> str:
        return f"""
            <div class="grid" style="text-align: center">
                <article>
                    <h2>internal</h2>
                    <canvas id="internal-thermometer" height="350" width="200">thermometer</canvas>
                    <br>
                    <strong>{self.records[0]["values"][0]}{self.unit}</strong>
                </article>
                <article>
                    <h2>DHT11</h2>
                    <canvas id="dht-thermometer" height="350" width="200">thermometer</canvas>
                    <br>
                    <strong>{self.records[0]["values"][1]}{self.unit}</strong>
                </article>
                <article>
                    <h2>BMP280</h2>
                    <canvas id="bmp-thermometer" height="350" width="200">thermometer</canvas>
                    <br>
                    <strong>{self.records[0]["values"][2]}{self.unit}</strong>
                </article>
            </div>
            <script>
                console.log("Loaded data for thermometer");
                var initialData = {json.dumps(self.records)};
            </script>
            <script src="js/thermometers.js"></script>
        """
