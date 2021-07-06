#!/bin/bash

set -e

echo "${0}: Running Adjutant..."
cd /usr/src/code/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop
adjutant-api migrate
adjutant-api runserver 0.0.0.0:5050