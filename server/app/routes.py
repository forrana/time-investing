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
    today = datetime.utcnow().date()
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    start_previous_week = start_week - timedelta(days=7)
    end_previous_week = start_previous_week + timedelta(days=6)
    skills = Skill.objects(owner=current_user.id).order_by("name")
    expenses = Expense.objects(owner=current_user.id, finished_at__ne='', date__gte=today, date__lt=tomorrow ).aggregate(
          {
            "$group": { "_id": "$skill", "total": { "$sum": "$amount" }, "name": { "$first": "$skill_name"}}
          }
        )
    current_week_expenses = Expense.objects(owner=current_user.id, finished_at__ne='', date__gte=start_week, date__lt=end_week ).aggregate(
          {
            "$group": { "_id": "$skill", "total": { "$sum": "$amount" }, "name": { "$first": "$skill_name"}}
          }
        )
    previous_week_expenses = Expense.objects(owner=current_user.id, finished_at__ne='', date__gte=start_previous_week, date__lt=end_previous_week ).aggregate(
          {
            "$group": { "_id": "$skill", "total": { "$sum": "$amount" }, "name": { "$first": "$skill_name"}}
          }
        )
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "home.html" %}
        {% endblock %}
        """, **{'skills': skills, \
                'expenses': JSONEncoder().encode(list(expenses)), \
                'current_week_expenses': JSONEncoder().encode(list(current_week_expenses)), \
                'previous_week_expenses': JSONEncoder().encode(list(previous_week_expenses)), \
                'default_time': current_user.default_time \
        })

@app.route('/settings')
@login_required
def settings():
    attributes = Attribute.objects(owner=current_user.id).order_by("name")
    skills = Skill.objects(owner=current_user.id).order_by("name")
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
