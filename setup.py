#!/usr/bin/env python

import os
import subprocess

venv_dir = 'venv'

if not os.path.isdir(venv_dir):
    subprocess.call(['virtualenv', venv_dir])

pip = venv_dir + '/bin/pip'

subprocess.call([pip, 'install', '-r', 'requirements.txt'])
