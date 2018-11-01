from app import app
from datetime import datetime
from flask_mongoengine import MongoEngine
from flask_user import UserMixin, UserManager
db = MongoEngine(app)

def fill_timestamps(self):
    if not self.creation_date:
        self.creation_date = datetime.now()
    self.modified_date = datetime.now()
    return self

class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)
    username = db.StringField(default='')
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    password = db.StringField()
    email = db.StringField()
    password = db.StringField()
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField()
    roles = db.ListField(db.StringField(), default=[])

    def save(self, *args, **kwargs):
        self = fill_timestamps(self)
        return super(User, self).save(*args, **kwargs)

user_manager = UserManager(app, db, User)

class Expense(db.Document):
    amount = db.StringField()
    date = db.DateTimeField()
    time = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    place = db.StringField()
    tags = db.ListField(db.StringField(), default=[])
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField()

    def save(self, *args, **kwargs):
        self = fill_timestamps(self)
        return super(Expense, self).save(*args, **kwargs)
