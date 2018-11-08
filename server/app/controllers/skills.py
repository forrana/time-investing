''' controller and routes for skills '''
import os
from flask import request, jsonify, url_for, redirect
from app import app, Skill, login_required, current_user
from datetime import datetime

@app.route('/api/skill/create', methods=['POST'])
@login_required
def skill_create():
    data = request.form.copy()
    if request.method == 'POST':
        if data.get('name', None) is not None:
            data['attributes'] = data.getlist('attributes')
            new_skill = Skill(**data)
            new_skill.save()
            return redirect(url_for('settings'))
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/skill/all', methods=['GET'])
@login_required
def skill_get():
    if request.method == 'GET':
        query = request.args
        data = Skill.objects(owner=current_user.id)
        return jsonify(data), 200

@app.route('/api/skill/delete/<id>', methods=['DELETE', 'POST'])
@login_required
def skill_delete(id):
    if id is not None:
        db_response = Skill.objects(id=id).delete()
        return redirect(url_for('settings'))
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/api/skill/update', methods=['PATCH'])
@login_required
def skill_update():
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            Skill.objects(data['query']).update_one(
                data['query'], {'$set': data.get('payload', {})})
            return redirect(url_for('settings'))
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
