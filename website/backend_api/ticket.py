from .. import auth, db
from flask_restful import Resource
from flask import request
from ..models import Verify, Ticket

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