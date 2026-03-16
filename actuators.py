"""
Actuator control classes.
"""

import RPi.GPIO as GPIO

class Relay:
    """Simple relay control."""
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        GPIO.output(self.pin, not GPIO.input(self.pin))

    def status(self):
        return GPIO.input(self.pin)