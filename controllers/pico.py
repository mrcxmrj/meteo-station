import time

from machine import Pin

led = Pin("LED", Pin.OUT)


def blink_led():
    led.value(1)
    time.sleep(0.5)
    led.value(0)


# def read_temperature():
