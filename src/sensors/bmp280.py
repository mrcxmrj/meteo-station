import time

from machine import I2C, Pin

from sensors.bmp280_driver import *


class BMP280:
    def __init__(self, sda_pin_number: int, scl_pin_number: int) -> None:
        self.sda_pin = Pin(sda_pin_number)
        self.scl_pin = Pin(scl_pin_number)
        self.bus = I2C(0, sda=self.sda_pin, scl=self.scl_pin, freq=400000)
        time.sleep(0.1)
        self.bmp = BMP280Driver(self.bus)
        self.bmp.use_case(BMP280_CASE_INDOOR)

    def read_pressure(self) -> float:
        try:
            pressure_pa = self.bmp.pressure
            pressure_hpa = pressure_pa / 100
            return pressure_hpa
        except OSError as e:
            print("Failed to read pressure from BMP280", e)
            return -999

    def read_temperature(self) -> float:
        try:
            return self.bmp.temperature
        except OSError as e:
            print("Failed to read temperature from BMP280", e)
            return -999
