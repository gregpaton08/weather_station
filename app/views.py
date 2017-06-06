from flask import render_template, jsonify
from app import app
import get_weather
import thermometer

@app.route('/')
@app.route('/index')
def index():
    # get forecast for next 12 hours
    hourly_forecast = get_weather.get_hourly_forecast(12)
    return render_template('index.html',
                           inside_temperature=round(thermometer.read_temp_f(), 0),
                           outside_temperature=round(get_weather.get_temperature(), 0),
                           condition=get_weather.get_condition().lower(),
                           hourly=hourly_forecast)


@app.route('/get_inside_temperature')
def get_inside_temperature():
    return jsonify(temperature=round(thermometer.read_temp_f(), 0))


@app.route('/get_outside_temperature')
def get_outside_temperature():
    return jsonify(temperature=round(get_weather.get_temperature(), 0))


@app.route('/get_sunrise')
def get_sunrise():
    return jsonify(sunrise=get_weather.get_sunrise())


@app.route('/get_sunset')
def get_sunset():
    return jsonify(sunrise=get_weather.get_sunset())


@app.route('/get_hourly_forecast')
def get_hourly_forecast():
    return jsonify(forecast=get_weather.get_hourly_forecast())