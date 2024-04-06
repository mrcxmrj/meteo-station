import time
from machine import Pin

led = Pin("LED", Pin.OUT)

def pico_blink_led ():
    led.value(1)
    time.sleep(0.5)
    led.value(0)
