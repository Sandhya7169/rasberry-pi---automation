"""
Utility functions.
"""

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def format_timestamp(timestamp):
    """Convert ISO timestamp to readable format."""
    from datetime import datetime
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = timestamp
    return dt.strftime("%Y-%m-%d %H:%M:%S")