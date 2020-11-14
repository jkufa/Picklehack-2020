#!/bin/sh
export FLASK_APP=__init__.py
export FLASK_ENV=development # Comment out when testing for production
flask run