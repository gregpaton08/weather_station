#!/usr/bin/env python

import os
import subprocess

if not os.path.isdir('flask'):
    subprocess.call('virtualenv flask'.split())

subprocess.call('flask/bin/pip install flask'.split())
subprocess.call('flask/bin/pip install flask-login'.split())
subprocess.call('flask/bin/pip install flask-openid'.split())
subprocess.call('flask/bin/pip install flask-mail'.split())
subprocess.call('flask/bin/pip install flask-sqlalchemy'.split())
subprocess.call('flask/bin/pip install sqlalchemy-migrate'.split())
subprocess.call('flask/bin/pip install flask-whooshalchemy'.split())
subprocess.call('flask/bin/pip install flask-wtf'.split())
subprocess.call('flask/bin/pip install flask-babel'.split())
subprocess.call('flask/bin/pip install guess_language'.split())
subprocess.call('flask/bin/pip install flipflop'.split())
subprocess.call('flask/bin/pip install coverage'.split())