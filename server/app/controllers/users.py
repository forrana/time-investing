''' controller and routes for users '''
import os
from flask import request, jsonify, redirect, url_for
from app import app, User, login_required

@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@login_required
def user():
    if request.method == 'GET':
        query = request.args
        data = User.objects(query)
        return jsonify(data), 200

    data = request.form
    if request.method == 'POST':
        if data.get('id', None) is not None and data.get('default_time', None) is not None:
            User.objects(id=data['id']).update_one(default_time=data.get('default_time'))
            return redirect(url_for('settings'))
        else:
            if data.get('email', None) is not None:
                User.objects(email=data['email']).insert_one(data)
                return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
            else:
                return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = User.objects(email=data['email']).delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
