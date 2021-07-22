from website import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class Verify(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_student = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(120), nullable = False)
    full_name = db.Column(db.String(40), nullable = False)
    username = db.Column(db.String(32), nullable = False)
    isreciept = db.Column(db.Boolean(), nullable = False, default = False)
    isgaucho = db.Column(db.Boolean(), nullable = False, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        data = {
            'id' : self.id,
            'type_student' : self.type_student,
            'email' : self.email,
            'full_name' : self.full_name,
            'username' : self.username,
            'isreciept' : self.isreciept,
            'isgaucho' : self.isgaucho,
            'date_created' : str(self.date_created)
            }
        return json.dumps(data)

class Removal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reason = db.Column(db.PickleType(), nullable = True)
    other_reason = db.Column(db.String, nullable = True)
    email = db.Column(db.String(120), nullable = False)
    username = db.Column(db.String(32), nullable = False)
    comments = db.Column(db.Text, nullable = True)
    isreciept = db.Column(db.Boolean(), nullable = False, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        data = {
            'id' : self.id,
            'reason' : self.reason,
            'other_reason' : self.other_reason,
            'email' : self.email,
            'username' : self.username,
            'comments' : self.comments,
            'isreciept' : self.isreciept,
            'date_created' : str(self.date_created)
        }
        return json.dumps(data)

class Emoji(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable = False)
    description = db.Column(db.Text, nullable = True)
    emoji_image = db.Column(db.Text, nullable = True)
    emoji_image_name = db.Column(db.Text, nullable = True)
    emoji_image_type = db.Column(db.Text, nullable = True)
    isinserver = db.Column(db.Boolean(), nullable = False, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        data = {
            'id' : self.id,
            'username' : self.username,
            'description' : self.description,
            'emoji_image' : 'http://127.0.0.1:5000/admin/image/' + str(self.id),
            'emoji_image_name' : self.emoji_image_name,
            'emoji_image_type' : self.emoji_image_type,
            'isinserver' : self.isinserver,
            'date_created' : str(self.date_created)
        }
        return json.dumps(data)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_ticket = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(32), nullable = False)
    against_username = db.Column(db.String(32), nullable = False)
    issue = db.Column(db.Text, nullable = True)
    isreciept = db.Column(db.Boolean(), nullable = False, default = False)
    isresolved = db.Column(db.Boolean(), nullable = False, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        data = {
            'id' : self.id,
            'type_ticket' : self.type_ticket,
            'username' : self.username,
            'against_username' : self.against_username,
            'issue' : self.issue,
            'isreciept' : self.isreciept,
            'isresolved' : self.isresolved,
            'date_created' : str(self.date_created)
        }
        return json.dumps(data)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    date_accessed = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"