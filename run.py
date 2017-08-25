#!flask/bin/python
# from app import app

# if __name__ == '__main__':
#     #app.run(host='0.0.0.0', port=4000, debug=False)
#     app.run(host='0.0.0.0', debug=False)

from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Yo, it''s working!'

if __name__ == "__main__":
    app.run()