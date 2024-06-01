import asyncio
import os

from sensors.bmp280 import BMP280
from sensors.dht11 import DHT11
from sensors.pico import Pico


class Reader:
    def __init__(
        self,
        board: Pico,
        humidity_temperature_sensor: DHT11,
        pressure_temperature_sensor: BMP280,
        output_path: str,
    ) -> None:
        self.board = board
        self.humidity_temperature_sensor = humidity_temperature_sensor
        self.pressure_temperature_sensor = pressure_temperature_sensor
        self.output_path = output_path

    def read_measurements(self) -> tuple[float, float, float, float]:
        board_temperature = round(self.board.read_temperature(), 2)
        temperature = round(self.humidity_temperature_sensor.read_temperature(), 2)
        humidity = round(self.humidity_temperature_sensor.read_humidity(), 2)
        pressure = round(self.pressure_temperature_sensor.read_pressure(), 2)
        return board_temperature, temperature, humidity, pressure

    def save_measurements(self, board_temperature, temperature, humidity) -> None:
        with open(self.output_path, "a+") as file:
            file.write(f"{board_temperature},{temperature},{humidity}\n")

    def read_saved_measurements(self, top: int) -> list[list[str]]:
        try:
            with open(self.output_path, "r") as file:
                lines = [line.rstrip().split(",") for line in list(file)]
                # FIXME: I think this is a bad idea for long list of records
                records = [
                    [board_temperature, sensor_temperature, sensor_humidity]
                    for board_temperature, sensor_temperature, sensor_humidity, *_ in lines[
                        -top:
                    ]
                ]
                return records
        except OSError:
            return []

    def clear_measurements(self) -> None:
        try:
            os.remove(self.output_path)
        except OSError:
            pass

    async def read_loop(self, frequency) -> None:
        while True:
            *measurements, pressure = self.read_measurements()
            print(f"pressure: {pressure}")
            print("Measurements made: ", *measurements)
            self.read_saved_measurements(10)
            self.save_measurements(*measurements)
            await asyncio.sleep(frequency)
