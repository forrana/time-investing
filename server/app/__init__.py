from flask import Flask, jsonify
from redis import Redis
from authlib.flask.client import OAuth

from loginpass import create_flask_blueprint
from loginpass import (
    Google, Facebook
)

from . import utils
from .utils import Cache

OAUTH_BACKENDS = [
    Facebook, Google
]

# Define the WSGI application object
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

# Configurations
app.config.from_object(__name__)
app.config.from_pyfile('config.py')

from . import models
from .models import User

oauth = OAuth(app, Cache())

@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))


def handle_authorize(remote, token, user_info):
    keys = ['family_name', 'given_name', 'email', 'picture']
    newUser = {x:user_info[x] for x in keys}
    User.objects(email=newUser['email'])\
        .update_one(**newUser, upsert=True)
    return jsonify(newUser)

for backend in OAUTH_BACKENDS:
    bp = create_flask_blueprint(backend, oauth, handle_authorize)
    app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))
