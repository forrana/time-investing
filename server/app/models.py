from app import app
import datetime
from flask_mongoengine import MongoEngine
db = MongoEngine(app)

class User(db.Document):
    picture = db.StringField()
    family_name = db.StringField()
    given_name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField(default=datetime.datetime.now)

def save(self, *args, **kwargs):
    if not self.creation_date:
        self.creation_date = datetime.datetime.now()
    self.modified_date = datetime.datetime.now()
    return super(User, self).save(*args, **kwargs)
