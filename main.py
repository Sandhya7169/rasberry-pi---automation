#!/usr/bin/env python3
"""
Main entry point for Raspberry Pi Home Automation Hub.
Starts sensor logging, web server, and actuator control threads.
"""

import threading
import time
import yaml
from sensors import read_dht22
from actuators import Relay
from database import Database
from web_server import app
import logging

logging.basicConfig(level=logging.INFO)

def sensor_logger(db, config):
    """Periodically read sensor and store in database."""
    interval = config['logging']['interval']
    while True:
        try:
            temp, hum = read_dht22(config['sensors']['dht22']['pin'])
            if temp is not None and hum is not None:
                db.insert_sensor_reading(temp, hum)
                logging.info(f"Logged: {temp:.1f}°C, {hum:.1f}%")
            else:
                logging.warning("Failed to read sensor")
        except Exception as e:
            logging.error(f"Sensor logger error: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    # Initialize database
    db = Database(config['database']['path'])
    db.create_tables()

    # Initialize relay
    relay = Relay(config['actuators']['light_relay']['pin'])

    # Start sensor logging in background thread
    logger_thread = threading.Thread(target=sensor_logger, args=(db, config), daemon=True)
    logger_thread.start()

    # Run Flask web server
    app.config['db'] = db
    app.config['relay'] = relay
    app.run(host=config['web']['host'], port=config['web']['port'], debug=config['web']['debug'])