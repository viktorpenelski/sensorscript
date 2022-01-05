#!/bin/bash

source venv2/Scripts/activate
set -a
source .env
set +a

python publish_sensors.py

exit 0