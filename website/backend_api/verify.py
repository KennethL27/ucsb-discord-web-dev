from .. import auth, db
from flask_restful import Resource
from flask import request
from ..models import Verify

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
        if action == 'update_role': 
            user = Verify.query.filter_by(username = values['username']).first()
            if not user:
                return {'status' : 'error: user not found'}, 404
            user.isrole =  user.type_user
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
            user.type_user = values['type']
            db.session.commit()
            return {'status' : 'complete'}, 200

        else:
            return {'status' : 'Not Valid'}, 406