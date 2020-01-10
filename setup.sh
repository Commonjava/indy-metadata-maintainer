#!/bin/bash

set -x

virtualenv --python=$(which python3) .venv

source .venv/bin/activate
pip install --upgrade pip
pip install .

