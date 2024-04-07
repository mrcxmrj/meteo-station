import time

from machine import ADC, Pin

led = Pin("LED", Pin.OUT)
temperature_sensor = ADC(4)

convert_adc_to_volt = lambda adc_value: (3.3 / 65535) * adc_value
convert_volt_to_celcius = lambda volt_value: 27 - (volt_value - 0.706) / 0.001721


def blink_led():
    led.value(1)
    time.sleep(0.5)
    led.value(0)


def read_temperature():
    volt_reading = convert_adc_to_volt(temperature_sensor.read_u16())
    temperature = convert_volt_to_celcius(volt_reading)
    return temperature
