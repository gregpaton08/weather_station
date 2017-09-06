from flask import render_template, jsonify, g, request
from app import app
import get_weather
import thermometer
import thermometer_db
from flask_httpauth import HTTPBasicAuth
import os

auth = HTTPBasicAuth()

@app.route('/')
@app.route('/index')
def index():
    # get forecast for next 12 hours
    hourly_forecast = get_weather.get_hourly_forecast(12)
    return render_template('index.html',
                           condition=get_weather.get_condition().lower(),
                           hourly=hourly_forecast)


@app.route('/get_temperature_data_c')
def get_temperature_date_c():
    return jsonify(inside_temperature=round(thermometer_db.get_temperature_c(get_db_connection()), 0),
                   outside_temperature=round(get_weather.get_temperature_c(), 0))


@app.route('/get_sunrise')
def get_sunrise():
    return jsonify(sunrise=get_weather.get_sunrise())


@app.route('/get_sunset')
def get_sunset():
    return jsonify(sunrise=get_weather.get_sunset())


@app.route('/get_hourly_forecast')
def get_hourly_forecast():
    return jsonify(forecast=get_weather.get_hourly_forecast())


@app.route('/get_hourly_indoor_history')
def get_hourly_indoor_history():
    print('Dir {0}'.format(os.getcwd()))
    thermometer_db.get_temperature_history()
    return jsonify(history=thermometer_db.get_temperature_history())


@app.route('/update_temperature', methods=['POST'])
@auth.login_required
def update_temperature():
    if not request.json or not 'temperature' in request.json:
        abort(400)
    thermometer_db.store_temperature(request.json['temperature'])
    return render_template('index.html'), 201


@auth.verify_password
def verify_password(username, password):
    return password == get_api_password()


def get_api_password():
    key = os.environ.get('REST_API_PASSWORD', None)
    if key:
        return key
    with open('api_password.txt') as file:
        return file.read().strip()
    return ''


def get_db_connection():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = thermometer_db.get_connection()
    return g.sqlite_db
