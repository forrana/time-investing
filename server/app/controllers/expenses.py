''' controller and routes for expenses '''
import os
from flask import request, jsonify, url_for, redirect
from app import app, Expense, login_required, current_user
from datetime import datetime

@app.route('/api/expense/create', methods=['POST'])
@login_required
def expense_create():
    data = request.form
    if request.method == 'POST':
        if data.get('amount', None) is not None:
            new_expense = Expense(**data)
            new_expense.save()
            return redirect(url_for('expenses_list_page'))
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
        return redirect(url_for('expenses_list_page'))
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/expense/update', methods=['PATCH'])
@login_required
def expense_update():
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            Expense.objects(data['query']).update_one(
                data['query'], {'$set': data.get('payload', {})})
            return redirect(url_for('expenses_list_page'))
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
