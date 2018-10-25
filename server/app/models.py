from app import app
from flask_mongoengine import MongoEngine
db = MongoEngine(app)

class User(db.Document):
    picture = db.StringField()
    family_name = db.StringField()
    given_name = db.StringField()
    email = db.StringField()
