from website import db
from datetime import datetime

class Verify(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_student = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(120), nullable = False)
    full_name = db.Column(db.String(40), nullable = False)
    username = db.Column(db.String(32), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"

class Removal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reason = db.Column(db.PickleType(), nullable = True)
    other_reason = db.Column(db.String, nullable = True)
    email = db.Column(db.String(120), nullable = False)
    username = db.Column(db.String(32), nullable = False)
    comments = db.Column(db.Text, nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"

class Emoji(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable = False)
    description = db.Column(db.Text, nullable = True)
    emoji_image = db.Column(db.LargeBinary, nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_ticket = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(32), nullable = False)
    against_username = db.Column(db.String(32), nullable = False)
    issue = db.Column(db.Text, nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"