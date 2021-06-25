from website import api, auth, db
from flask_restful import Resource
from flask import request, jsonify
from website.models import Verify
import os, json

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
        for db_input in values:
            if db_input == 'username':
                user = Verify.query.filter_by(username = values[db_input]).first()
                return str(user), 200 # Return the database row of the specfic user along with status code of 200
            elif db_input == 'id_len':
                return len(Verify.query.all()), 200
            elif db_input == 'id':
                user = Verify.query.filter_by(id = values[db_input]).first()
                return str(user), 200
            elif type(db_input) == str:
                return {'status' : 'invalid'}, 406
            else:
                return {'status': 'Not Found'}, 404
            
    
    @auth.login_required
    def post(self):
        values = request.json
        if values['action'] == 'update_gaucho':
            user = Verify.query.filter_by(username = values['username']).first()
            user.isgaucho = True
            db.session.commit()
            return {'status' : 'complete'}, 200
        return 

class Ticket_API(Resource):
    @auth.login_required
    def get(self):
        values = request.json

api.add_resource(Verify_API, '/verify')
api.add_resource(Ticket_API, '/ticket')