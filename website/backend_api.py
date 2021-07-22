from requests.sessions import session
from website import api, auth, db
from flask_restful import Resource
from flask import request, jsonify
from website.models import Verify, Ticket, Removal, Emoji
import os

secret_token = os.environ.get('SECRET_KEY')
TOKEN = {
    'token' : secret_token
}

@auth.verify_token
def verify_token(token):
    if token in TOKEN['token']:
        return token

class Verify_API(Resource):
    @auth.login_required
    def get(self):
        values = request.json
        action = values['action']
        if action == 'username':
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: username not found'}, 404
            return str(user), 200 
        elif action == 'id_len':
            return len(Verify.query.all()), 200
        elif action == 'id':
            user = Verify.query.filter_by(id = values['id']).first()
            return str(user), 200
        else:
            return {'status' : 'invalid'}, 406            
    
    @auth.login_required
    def post(self):
        values = request.json
        action = values['action']
        if action == 'update_gaucho':
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: user not found'}, 404
            user.isgaucho = True
            db.session.commit()
            return {'status' : 'complete'}, 200

        elif action == 'update_email':
            check = Verify.query.filter_by(email = values['update_email']).first()
            if check:
                return {'status' : 'error: email already exist'}, 406
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: user not found'}, 404
            user.email = values['update_email']
            db.session.commit()
            return {'status' : 'complete'}, 200

        elif action == 'update_name':
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: user not found'}, 404
            user.full_name = values['name']
            db.session.commit()
            return {'status' : 'complete'}, 200
        
        elif action == 'update_type':
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: user not found'}, 404
            user.type_student = values['type']
            db.session.commit()
            return {'status' : 'complete'}, 200

        else:
            return {'status' : 'Not Valid'}, 406

class Ticket_API(Resource):
    @auth.login_required
    def get(self):
        values = request.json
        action = values['action']
        if action == 'unresolved':
            unresolved_list = Ticket.query.filter_by(isresolved = False).all()
            unresolved_ids = [id.id for id in unresolved_list]
            return {'unresolved_ids' : unresolved_ids}, 200

        elif values['id'] == None:
            ids = db.session.query(Ticket.id).all()
            id_column = [id for id, in ids]
            return {'ids' : id_column}, 200
        
        elif action == 'id':
            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            return str(entry), 200

        else:
            return {'status' : 'Not Valid'}, 406

    @auth.login_required
    def post(self):
        values = request.json
        action = values['action']
        if action == 'isresolved':
            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            entry.isresolved = values['isresolved']
            db.session.commit()
            return {'status' : 'complete'}, 200
        
        elif action == 'update_username':
            check = Verify.query.filter_by(username = values['new_username']).first()
            if not check:
                return {'status' : 'error: user not find new username in database'}, 404

            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            entry.username = values['new_username']
            db.session.commit()
            return {'status' : 'complete'}, 200
        
        elif action == 'update_against_username':
            check = Verify.query.filter_by(username = values['new_against_username']).first()
            if not check:
                return {'status' : 'error: user not find new against username in database'}, 404

            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            entry.against_username = values['new_against_username']
            db.session.commit()
            return {'status' : 'complete'}, 200

        elif action == 'update_type':
            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            entry.type_ticket = values['update_type']
            db.session.commit()
            return {'status' : 'complete'}, 200

        elif action == 'append_issue':
            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            initial_issue = entry.issue
            appended_issue = initial_issue + 'Appended: ' + values['append_issue']
            entry.issue = appended_issue
            db.session.commit()
            return {'status' : 'complete'}, 200

        elif action == 'update_issue':
            entry = Ticket.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            entry.issue = values['update_issue']
            db.session.commit()
            return {'status' : 'complete'}, 200

        else:
            return {'status' : 'Not Valid'}, 406

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

class Emoji_API(Resource):
    @auth.login_required
    def get(self):
        values = request.json
        action = values['action']
    
        if action == 'id':
            entry = Emoji.query.filter_by(id = values['id']).first()
            if not entry:
                return {'status' : 'error: entry not found'}, 404
            return str(entry), 200

        elif action == 'inserver':
            inserver_list = Emoji.query.filter_by(isinserver = values['inserver']).all()
            inserver_ids = [id.id for id in inserver_list]
            return {'inserver_ids' : inserver_ids}, 200

        elif action == 'ids':
            emoji_list = db.session.query(Emoji.id).all()
            emoji_ids = [entry.id for entry in emoji_list]
            return {'ids' : emoji_ids}, 200

        else:
            return {'status' : 'Not Valid'}, 406
    
    @auth.login_required
    def post(self):
        values = request.json
        action = values['action']
        if action == 'isinserver':
            entry = Emoji.query.filter_by(id = values['id']).first()
            entry.isinserver = values['isinserver']
            db.session.commit()
            return {'status' : 'complete'}, 200
            
        elif action == 'delete_entry':
            entry = db.session.query(Emoji).filter_by(id = values['id']).delete()
            db.session.commit()
            return {'status' : 'complete'}, 200

        else:
            return {'status' : 'Not Valid'}, 406

api.add_resource(Verify_API, '/verify')
api.add_resource(Ticket_API, '/ticket')
api.add_resource(Removal_API, '/removal')
api.add_resource(Emoji_API, '/emoji')