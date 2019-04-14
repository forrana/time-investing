from datetime import datetime, timedelta
import json
from bson import ObjectId
from app import *

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
@login_required
def home():
    skills = Skill.objects(owner=current_user.id, deleted_at='').order_by("name")
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "home/home.html" %}
        {% endblock %}
        """, **{'skills': skills, \
                'default_time': current_user.default_time \
        })

@app.route('/settings')
@login_required
def settings():
    attributes = Attribute.objects(owner=current_user.id, deleted_at='').order_by("name")
    skills = Skill.objects(owner=current_user.id, deleted_at='').order_by("name")
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "settings/settings.html" %}
        {% endblock %}
        """, **{'attributes': attributes, 'skills': skills, 'id': current_user.id, \
            'default_time': current_user.default_time})

@app.route('/time_log')
@login_required    # User must be authenticated
def time_log():
    expenses = Expense.objects(owner=current_user.id, finished_at__ne='')
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
