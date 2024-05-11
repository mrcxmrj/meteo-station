import dht
from machine import Pin


class DHT11:
    def __init__(self, pin_number) -> None:
        self.pin = Pin(pin_number)
        self.sensor = dht.DHT11(self.pin)

    def read_temperature(self) -> int:
        try:
            self.sensor.measure()
            return self.sensor.temperature()
        except OSError as e:
            print("Failed to read temperature from DHT11", e)
            return -999

    def read_humidity(self) -> int:
        try:
            self.sensor.measure()
            return self.sensor.humidity()
        except OSError as e:
            print("Failed to read humidity from DHT11", e)
            return -999
