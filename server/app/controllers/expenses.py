''' controller and routes for expenses '''
import os
from flask import request, jsonify, url_for, redirect
from app import app, Expense, login_required, current_user
from datetime import datetime

@app.route('/api/expense/create', methods=['POST'])
@login_required
def expense_create():
    data = request.get_json()
    if request.method == 'POST':
        if data.get('skill', None) is not None:
            new_expense = Expense(**data)
            new_expense.started_at = datetime.strptime(data.get('started_at'), '%Y-%m-%dT%H:%M:%S')
            new_expense.save()
            return jsonify({ 'ok': True, 'expense': new_expense }), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

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
