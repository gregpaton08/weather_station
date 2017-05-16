from flask import render_template
from app import app
import get_weather

@app.route('/')
@app.route('/index')
def index():
    # get forecast for next 12 hours
    hourly_forecast = get_weather.get_hourly_forecast()[:12]
    return render_template('index.html',
                           temperature=get_weather.get_temperature(),
                           hourly=hourly_forecast)