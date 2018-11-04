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
from .models import User, user_manager, Expense
from app.controllers import *

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            <h2>Home page</h2>
        {% endblock %}
        """)

# The Members page is only accessible to authenticated users via the @login_required decorator
@app.route('/members')
@login_required    # User must be authenticated
def member_page():
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            <h2>Members page</h2>
        {% endblock %}
        """)

# The Members page is only accessible to authenticated users via the @login_required decorator
@app.route('/expense')
@login_required    # User must be authenticated
def expense_page():
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "expenses.html" %}
        {% endblock %}
        """)

@app.route('/expenses')
@login_required    # User must be authenticated
def expenses_list_page():
    expenses = Expense.objects(owner=current_user.id).order_by("-date","name")
    # String-based templates
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "expenses-list.html" %}
        {% endblock %}
        """, **{'expenses': expenses, 'current_date': datetime.now().strftime("%Y-%m-%d")})
