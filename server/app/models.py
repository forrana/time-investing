from app import app, current_user
from datetime import datetime
from flask_mongoengine import MongoEngine
from flask_user import UserMixin, UserManager
db = MongoEngine(app)

def fill_timestamps(self):
    if not self.created_at:
        self.created_at = datetime.now()
    self.updated_at = datetime.now()
    return self

class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)
    username = db.StringField(default='')
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    password = db.StringField()
    email = db.StringField()
    password = db.StringField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    default_time = db.StringField(default_time=0)
    roles = db.ListField(db.StringField(), default=[])

    def save(self, *args, **kwargs):
        fill_timestamps(self)
        return super(User, self).save(*args, **kwargs)

user_manager = UserManager(app, db, User)


class TimeStampsOwnerModel(db.Document):
    meta = {
        'abstract': True
    }

    updated_at = db.DateTimeField(default=datetime.now)
    created_at = db.DateTimeField(default=datetime.now)
    owner = db.ReferenceField(User)

    def save(self, *args, **kwargs):
        fill_timestamps(self)
        self.owner = current_user.id
        return super(TimeStampsOwnerModel, self).save(*args, **kwargs)

class SafeDeletionModel(db.Document):
    meta = {
        'abstract': True
    }
    deleted_at = db.DateTimeField()

class Attribute(TimeStampsOwnerModel, SafeDeletionModel):
    name = db.StringField()

class Skill(TimeStampsOwnerModel, SafeDeletionModel):
    name = db.StringField()
    description = db.StringField()
    target_day = db.FloatField(default=0)
    target_week = db.FloatField(default=0)
    target_month = db.FloatField(default=0)
    target_year = db.FloatField(default=0)
    color = db.StringField()
    attributes = db.ListField(db.ReferenceField(Attribute))

    def stringify_attributes(self):
        if self.attributes:
            return ", ".join(map(lambda skill: skill["name"], self.attributes))
        return ""

class Expense(TimeStampsOwnerModel):
    skill_name = db.StringField()
    amount = db.DecimalField()
    date = db.DateTimeField(default=datetime.now)
    time = db.StringField()
    place = db.StringField()
    skill = db.ReferenceField(Skill)
    started_at = db.DateTimeField()
    finished_at = db.DateTimeField()

    def save(self, *args, **kwargs):
        if(self.skill):
            self.skill_name = self.skill.name
        return super(Expense, self).save(*args, **kwargs)
