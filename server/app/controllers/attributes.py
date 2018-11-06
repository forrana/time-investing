''' controller and routes for attributes '''
import os
from flask import request, jsonify, url_for, redirect
from app import app, Attribute, login_required, current_user
from datetime import datetime

@app.route('/api/attribute/create', methods=['POST'])
@login_required
def attribute_create():
    data = request.form
    if request.method == 'POST':
        if data.get('name', None) is not None:
            new_attribute = Attribute(**data)
            new_attribute.save()
            return redirect(url_for('settings'))
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/attribute/all', methods=['GET'])
@login_required
def attribute_get():
    if request.method == 'GET':
        query = request.args
        data = Attribute.objects(owner=current_user.id)
        return jsonify(data), 200

@app.route('/api/attribute/delete/<id>', methods=['DELETE', 'POST'])
@login_required
def attribute_delete(id):
    if id is not None:
        db_response = Attribute.objects(id=id).delete()
        return redirect(url_for('settings'))
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/attribute/update', methods=['PATCH'])
@login_required
def attribute_update():
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            Attribute.objects(data['query']).update_one(
                data['query'], {'$set': data.get('payload', {})})
            return redirect(url_for('settings'))
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
