from flask import Flask, g

app = Flask(__name__)
from weatherstation import views


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
