import dht
from machine import Pin

pin = Pin(28)
sensor = dht.DHT11(pin)


def read_temperature():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        return temperature
    except OSError as e:
        print("Failed to read from DHT11", e)
