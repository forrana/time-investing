''' controller and routes for expenses '''
import os
from flask import request, jsonify
from app import app, Expense

@app.route('/expense', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def expense():
    if request.method == 'GET':
        query = request.args
        data = Expense.objects(id=request.args['id'])
        return jsonify(data), 200

    data = request.form
    if request.method == 'POST':
        if data.get('name', None) is not None:
            new_expense = Expense(**data)
            new_expense["tags"] = data["tags"].split(',')
            new_expense.save()
            return jsonify({'ok': True, 'message': 'Expense created successfully!{}'.format(new_expense.id)}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('_id', None) is not None:
            db_response = Expense.objects(_id=data['_id']).delete_one({'_id': data['_id']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            Expense.objects(data['query']).update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
