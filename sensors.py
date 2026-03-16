"""
Sensor reading functions.
"""

import Adafruit_DHT

def read_dht22(pin):
    """Read temperature and humidity from DHT22 sensor.
    Returns (temperature, humidity) in degrees C and percent.
    """
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    return temperature, humidity