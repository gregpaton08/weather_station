#!/usr/bin/env bash

# get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}/..

venv_dir="venv"
if [ ! -d "$venv_dir" ]; then
    virtualenv $venv_dir
    sh ${DIR}/install_rf24.sh

    ${venv_dir}/bin/pip install -r requirements.txt
fi
