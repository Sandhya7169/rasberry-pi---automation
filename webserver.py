"""
Flask web server for dashboard and API.
"""

from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # We'll create a simple template inline for simplicity

@app.route('/api/sensors/latest')
def latest_sensor():
    db = app.config['db']
    data = db.get_latest_sensor_reading()
    return jsonify(data)

@app.route('/api/sensors/history')
def sensor_history():
    db = app.config['db']
    limit = request.args.get('limit', 100, type=int)
    data = db.get_sensor_readings(limit)
    return jsonify(data)

@app.route('/api/actuators/light', methods=['GET', 'POST'])
def light_control():
    relay = app.config['relay']
    if request.method == 'POST':
        action = request.json.get('action')
        if action == 'on':
            relay.on()
        elif action == 'off':
            relay.off()
        elif action == 'toggle':
            relay.toggle()
        return jsonify({'status': relay.status()})
    else:
        return jsonify({'status': relay.status()})

# Simple inline template for demo purposes (in real project, use separate files)
@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Automation</title>
        <script>
        function update() {
            fetch('/api/sensors/latest')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('temp').innerText = data.temperature.toFixed(1);
                    document.getElementById('hum').innerText = data.humidity.toFixed(1);
                    document.getElementById('time').innerText = new Date(data.timestamp).toLocaleString();
                });
            fetch('/api/actuators/light')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('light-status').innerText = data.status ? 'ON' : 'OFF';
                });
        }
        setInterval(update, 5000);
        window.onload = update;
        </script>
    </head>
    <body>
        <h1>Raspberry Pi Home Automation</h1>
        <h2>Latest Sensor Reading</h2>
        <p>Temperature: <span id="temp">--</span> °C</p>
        <p>Humidity: <span id="hum">--</span> %</p>
        <p>Last updated: <span id="time">--</span></p>
        <h2>Light Control</h2>
        <p>Light is <span id="light-status">--</span></p>
        <button onclick="fetch('/api/actuators/light', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'on'})}).then(update)">Turn On</button>
        <button onclick="fetch('/api/actuators/light', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'off'})}).then(update)">Turn Off</button>
    </body>
    </html>
    '''