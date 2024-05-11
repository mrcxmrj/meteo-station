import time

from machine import ADC, Pin


class Pico:
    def __init__(self) -> None:
        self.led = Pin("LED", Pin.OUT)
        self.temperature_sensor = ADC(4)

    def convert_adc_to_volt(self, adc_value: float) -> float:
        return (3.3 / 65535) * adc_value

    def convert_volt_to_celcius(self, volt_value: float) -> float:
        return 27 - (volt_value - 0.706) / 0.001721

    def blink_led(self) -> None:
        self.led.value(1)
        time.sleep(0.5)
        self.led.value(0)

    def read_temperature(self):
        volt_reading = self.convert_adc_to_volt(self.temperature_sensor.read_u16())
        temperature = self.convert_volt_to_celcius(volt_reading)
        return temperature
