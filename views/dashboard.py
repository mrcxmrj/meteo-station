class DashboardView:
    def generate_template(
        self,
        board_temperature: float,
        sensor_temperature: float,
        sensor_humidity: float,
    ) -> str:
        board_temperature = round(board_temperature, 2)
        sensor_temperature = round(sensor_temperature, 2)
        sensor_humidity = round(sensor_humidity, 2)
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
    <div class="container">

        <div class="grid">
            <article>
                <h2>Temperature</h2>
                <hr>
                <b>DHT11:</b> {sensor_temperature}°C
                <br>
                <b>internal sensor:</b> {board_temperature}°C
            </article>
            <article>
                <h2>Humidity</h2>
                <hr>
                <b>DHT11:</b> {sensor_humidity}%
            </article>
        </div>

    </div>
</body>

</html>
        """
