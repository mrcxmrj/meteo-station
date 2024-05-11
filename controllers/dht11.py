import dht
from machine import Pin


class DHT11:
    def __init__(self) -> None:
        self.pin = Pin(28)
        self.sensor = dht.DHT11(self.pin)

    def read_temperature(self) -> int:
        try:
            self.sensor.measure()
            return self.sensor.temperature()
        except OSError as e:
            print("Failed to read from DHT11", e)
            return -1
