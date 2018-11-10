from flask import Flask, jsonify, make_response, render_template_string, url_for
from redis import Redis
from flask_user import login_required, current_user
import os
import sys
from datetime import datetime

from . import utils
from .utils import Cache


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# Define the WSGI application object
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

# Configurations
app.config.from_object(__name__)
app.config.from_pyfile('config.py')
from . import models
from .models import User, user_manager, Expense, Attribute, Skill
from app.controllers import *

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
@login_required
def home():
    skills = Skill.objects(owner=current_user.id).order_by("name")
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "home.html" %}
        {% endblock %}
        """, **{'skills': skills})

@app.route('/settings')
@login_required
def settings():
    attributes = Attribute.objects(owner=current_user.id).order_by("name")
    skills = Skill.objects(owner=current_user.id).order_by("name")
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "settings.html" %}
        {% endblock %}
        """, **{'attributes': attributes, 'skills': skills})

@app.route('/time_log')
@login_required    # User must be authenticated
def time_log():
    expenses = Expense.objects(owner=current_user.id).order_by("-date","name")
    skills = Skill.objects(owner=current_user.id).order_by("name")
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "expenses-list.html" %}
        {% endblock %}
        """, **{
            'expenses': expenses,
            'current_date': datetime.now().strftime("%Y-%m-%d"),
            'skills': skills
            })
