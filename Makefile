# Needed for the "source" command to work properly
SHELL:=/bin/bash

init:
	python -m venv ./env
	source ./env/bin/activate && pip install -r requirements.txt --use-feature=2020-resolver

run:
	source ./env/bin/activate && ./main.py
