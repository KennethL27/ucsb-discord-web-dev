from .. import auth, db
from flask_restful import Resource
from flask import request
from ..models import Removal

class Removal_API(Resource):
    @auth.login_required
    def get(self):
        values = request.json
        action = values['action']

        if action == 'reasons':
            reasons_list = db.session.query(Removal.reason).all()
            reasons = [entry.reason for entry in reasons_list]
            other_reasons = [entry.other_reasons for entry in reasons_list]
            return {'reasons' : reasons, 'other_reasons' : other_reasons}, 200

        elif action == 'usernames':
            username_list = db.session.query(Removal.username).all()
            usernames = [entry.username for entry in username_list]
            return {'usernames' : usernames}, 200
        
        elif action == 'ids':
            removal_list = db.session.query(Removal.id).all()
            removal_ids = [entry.id for entry in removal_list]
            return {'ids' : removal_ids}, 200

        elif action == 'username':
            entry = Removal.query.filter_by(username = values['username']).first()
            if not entry:
                return {'status' : 'error: username not found'}, 404
            return str(entry), 200

        else:
            return {'status' : 'Not Valid'}, 406