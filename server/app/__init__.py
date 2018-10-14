# Import flask and template operators
from flask import Flask, render_template

from loginpass import create_flask_blueprint
from loginpass import (
    Google, Facebook
)

OAUTH_BACKENDS = [
    Facebook, Google
]

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_pyfile('config.py')
