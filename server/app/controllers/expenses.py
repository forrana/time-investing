''' controller and routes for expenses '''
import os
from flask import request, jsonify, url_for, redirect
from app import app, Expense, login_required, current_user
from datetime import datetime, timedelta
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/api/expense/create', methods=['POST'])
@login_required
def expense_create():
    data = request.get_json()
    if request.method == 'POST':
        if data.get('skill', None) is not None:
            if data.get('id', None) is not None:
                del data['id']
            new_expense = Expense(**data)
            new_expense.started_at = datetime.strptime(data.get('started_at'), '%Y-%m-%dT%H:%M:%S')
            if new_expense.finished_at is not None:
                new_expense.finished_at = datetime.strptime(data.get('finished_at'), '%Y-%m-%dT%H:%M:%S')
            new_expense.save()
            return jsonify({ 'ok': True, 'expense': new_expense }), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/expense/create_from_form', methods=['POST'])
@login_required
def expense_create_from_form():
    data = request.form
    if request.method == 'POST':
        if data.get('skill', None) is not None and request.form is not None:
            if data.get('id', None) is not None:
                del data['id']
            new_expense = Expense(**data)
            started_at = "{0}T{1}".format(data.get('date'), data.get('started_at'))
            finished_at = "{0}T{1}".format(data.get('date'), data.get('finished_at'))
            new_expense.started_at = datetime.strptime(started_at, '%Y-%m-%dT%H:%M')
            new_expense.finished_at = datetime.strptime(finished_at, '%Y-%m-%dT%H:%M')
            new_expense.save()
            return redirect(url_for('time_log'))
        else:
            return redirect(url_for('time_log'))

@app.route('/api/expense/all', methods=['GET'])
@login_required
def expense_get():
    if request.method == 'GET':
        query = request.args
        data = Expense.objects(owner=current_user.id)
        return jsonify(data), 200

@app.route('/api/expense/delete/<id>', methods=['DELETE', 'POST'])
@login_required
def expense_delete(id):
    if id is not None:
        db_response = Expense.objects(id=id).delete()
        return redirect(url_for('time_log'))
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/expense/update/<id>', methods=['POST'])
@login_required
def expense_update(id):
    data = request.get_json()
    if request.method == 'POST':
        if id is not None and data is not None:
            finished_at = datetime.strptime(data.get("finished_at"), '%Y-%m-%dT%H:%M:%S')
            if finished_at is not None:
                db_response = Expense.objects(id=id).update(finished_at = finished_at)
                return jsonify({'ok': True, 'message': db_response}), 200
            else:
                return jsonify({'ok': False, 'message': 'Parsin params error!'}), 400
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/expense/groups/<start_date_str>/<end_date_str>/', methods=['GET'])
@login_required
def expense_groups(start_date_str, end_date_str):
    if request.method == 'GET':
        if start_date_str is not None:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str is not None:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            else:
                end_date = start_date + timedelta(days=1)
            expense_groups = Expense.objects(owner=current_user.id, finished_at__ne='', date__gte=start_date, date__lt=end_date ).aggregate(
                  {
                    "$group": { "_id": "$skill", "total": { "$sum": "$amount" }, "name": { "$first": "$skill_name"}}
                  }
                )
            return jsonify({'ok': True, 'expense_groups': JSONEncoder().encode(list( expense_groups)) }), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
