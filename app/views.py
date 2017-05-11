from flask import render_template
from app import app
import get_weather

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           temperature=get_weather.get_temperature())