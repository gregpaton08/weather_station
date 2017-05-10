from app import app
import get_weather

@app.route('/')
@app.route('/index')
def index():
    html = '<h1>'
    html += str(get_weather.get_temperature())
    html += '&deg;</h1>'
    return html