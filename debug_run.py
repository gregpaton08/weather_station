#!venv/bin/python

from weatherstation import app
import sys

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
    #app.run(port=sys.argv[1])
