from .. import auth, db
from flask_restful import Resource
from flask import request
from ..models import Emoji

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