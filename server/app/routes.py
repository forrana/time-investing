from datetime import datetime, timedelta
from app import *

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
@login_required
def home():
    today = datetime.utcnow().date()
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    skills = Skill.objects(owner=current_user.id).order_by("name")
    expenses = Expense.objects(owner=current_user.id, finished_at__ne='', date__gte=today, date__lt=tomorrow ).aggregate(
          {
            "$group": { "_id": "$skill", "total": { "$sum": "$amount" }, "name": { "$first": "$skill_name"}}
          }
        )
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            {% include "home.html" %}
        {% endblock %}
        """, **{'skills': skills, 'expenses': expenses})

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
