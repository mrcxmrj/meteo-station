import asyncio
import os
import time

from sensors.bmp280 import BMP280
from sensors.dht11 import DHT11
from sensors.pico import Pico


class Reader:
    def __init__(
        self,
        board: Pico,
        humidity_temperature_sensor: DHT11,
        pressure_temperature_sensor: BMP280,
        output_directory: str,
    ) -> None:
        self.board = board
        self.humidity_temperature_sensor = humidity_temperature_sensor
        self.pressure_temperature_sensor = pressure_temperature_sensor
        try:
            os.mkdir(output_directory)
        except:
            pass
        self.output_path = output_directory + "/output.txt"
        self.temperature_output_path = output_directory + "/temperature.txt"
        self.humidity_output_path = output_directory + "/humidity.txt"
        self.pressure_output_path = output_directory + "/pressure.txt"

    def read_measurements(self) -> tuple[float, float, float, float, float]:
        board_temperature = round(self.board.read_temperature(), 2)

        ht_sensor_humidity = round(self.humidity_temperature_sensor.read_humidity(), 2)
        ht_sensor_temperature = round(
            self.humidity_temperature_sensor.read_temperature(), 2
        )

        pt_sensor_pressure = round(self.pressure_temperature_sensor.read_pressure(), 2)
        pt_sensor_temperature = round(
            self.humidity_temperature_sensor.read_temperature(), 2
        )

        return (
            board_temperature,
            ht_sensor_humidity,
            ht_sensor_temperature,
            pt_sensor_pressure,
            pt_sensor_temperature,
        )

    def read_saved_measurements_by_category(
        self, category: str = "all", top: int = 0
    ) -> list[dict[str, str | list[str]]]:
        if category == "temperature":
            return self.read_saved_measurements(self.temperature_output_path, top)
        elif category == "humidity":
            return self.read_saved_measurements(self.humidity_output_path, top)
        elif category == "pressure":
            return self.read_saved_measurements(self.pressure_output_path, top)
        else:
            return []

    def read_saved_measurements(
        self, output_path: str, top: int = 0
    ) -> list[dict[str, str | list[str]]]:
        try:
            with open(output_path, "r") as file:
                lines = [line.rstrip().split("|") for line in list(file)]
                return [
                    {"time": timestamp, "values": values.split(",")}
                    for timestamp, values, *_ in lines[-top:]
                ]
        except OSError:
            return []

    def save_measurements_for_category(self, output_path: str, content: str) -> None:
        # (year, month, mday, hour, minute, second, *_) = time.localtime()
        # timestamp = f"{year}-{month}-{mday} {hour}:{minute}:{second}"
        timestamp = time.time()
        with open(output_path, "a+") as file:
            file.write(str(timestamp) + "|" + content)

    def save_measurements(
        self,
        board_temperature: float,
        ht_sensor_humidity: float,
        ht_sensor_temperature: float,
        pt_sensor_pressure: float,
        pt_sensor_temperature: float,
    ) -> None:
        with open(self.output_path, "a+") as file:
            file.write(
                f"{board_temperature},{ht_sensor_humidity},{ht_sensor_temperature},{pt_sensor_pressure},{pt_sensor_temperature}\n"
            )
        self.save_measurements_for_category(
            self.temperature_output_path,
            f"{board_temperature},{ht_sensor_temperature},{pt_sensor_temperature}\n",
        )
        self.save_measurements_for_category(
            self.humidity_output_path, f"{ ht_sensor_humidity }\n"
        )
        self.save_measurements_for_category(
            self.pressure_output_path, f"{ pt_sensor_pressure }\n"
        )

    def clear_measurements(self) -> None:
        try:
            os.remove(self.output_path)
            os.remove(self.temperature_output_path)
            os.remove(self.humidity_output_path)
            os.remove(self.pressure_output_path)
        except OSError:
            print("Error clearing measurements")
            pass

    async def read_loop(self, frequency) -> None:
        while True:
            measurements = self.read_measurements()
            print("Measurements made: ", *measurements)
            self.save_measurements(*measurements)
            await asyncio.sleep(frequency)
