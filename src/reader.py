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

    def save_timed_measurements(self, output_path: str, content: str) -> None:
        (year, month, mday, hour, minute, *_) = time.localtime()
        timestamp = f"{year}-{month}-{mday} {hour}:{minute}"
        with open(output_path, "a+") as file:
            file.write(timestamp + "|" + content)
        pass

    def read_saved_timed_measurements(
        self, output_path: str, top: int
    ) -> list[dict[str, str]]:
        try:
            with open(output_path, "r") as file:
                lines = [line.rstrip().split("|") for line in list(file)]
                return [
                    {"time": timestamp, "values": values}
                    for timestamp, values in lines[-top:]
                ]
        except OSError:
            return []

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
        self.save_timed_measurements(
            self.temperature_output_path,
            f"{board_temperature},{ht_sensor_temperature},{pt_sensor_temperature}\n",
        )
        self.save_timed_measurements(self.humidity_output_path, str(ht_sensor_humidity))
        self.save_timed_measurements(self.pressure_output_path, str(pt_sensor_pressure))

    def read_saved_measurements(self, top: int) -> list[list[str]]:
        try:
            with open(self.output_path, "r") as file:
                lines = [line.rstrip().split(",") for line in list(file)]
                # FIXME: I think this is a bad idea for long list of records
                records = [
                    [
                        board_temperature,
                        ht_sensor_humidity,
                        ht_sensor_temperature,
                        pt_sensor_pressure,
                        pt_sensor_temperature,
                    ]
                    for board_temperature, ht_sensor_humidity, ht_sensor_temperature, pt_sensor_pressure, pt_sensor_temperature, *_ in lines[
                        -top:
                    ]
                ]
                return records
        except OSError:
            return []

    def read_saved_measurements_by_category(
        self, top: int
    ) -> tuple[list[list[str]], list[list[str]], list[list[str]]]:
        temperature_records: list[list[str]] = []
        humidity_records: list[list[str]] = []
        pressure_records: list[list[str]] = []

        records = self.read_saved_measurements(top)
        for record in records:
            temperature_records.append([record[0], record[2], record[4]])
            humidity_records.append([record[1]])
            pressure_records.append([record[3]])
        return temperature_records, humidity_records, pressure_records

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
            timed_measurements = self.read_saved_timed_measurements(
                self.temperature_output_path, 5
            )
            print("Saved temperature: " + str(timed_measurements))
            self.read_saved_measurements(10)
            self.save_measurements(*measurements)
            await asyncio.sleep(frequency)
