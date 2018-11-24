from flask import Flask, jsonify, make_response, render_template_string, url_for
from redis import Redis
from flask_user import login_required, current_user
import os
import sys
from datetime import datetime, timedelta

from . import utils
from .utils import Cache


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# Define the WSGI application object
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='[[',
        variable_end_string=']]',
    ))

app = CustomFlask(__name__)
redis = Redis(host='redis', port=6379)

# Configurations
app.config.from_object(__name__)
app.config.from_pyfile('config.py')

from . import models
from .models import User, user_manager, Expense, Attribute, Skill
from app.controllers import *
from . import routes
