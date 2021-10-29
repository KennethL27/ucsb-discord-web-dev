from .setup import base_url, get_request, post_request
import json

url = base_url + 'ticket'

class TicketEntry():
    def __init__(self, id : int = None, unresolved : bool = False ):
        json_package = {
            'action' : None,
            'id' : None
        }

        # get all unresolved entries
        if unresolved:
            json_package['action'] = 'unresolved'
            response = get_request(json_package, url).json()
            self.ids = response['unresolved_ids']
            self.status = response.status_code
            return

        # Getting all entry ids if no id is given
        if not id:
            response = get_request(json_package, url).json()
            self.ids = response['ids']
            self.status = response.status_code
            return 

        # view ticket        
        else:
            json_package['action'] = 'id'
            json_package['id'] = id
            response = get_request(json_package, url)
            if response.status_code == 404:
                raise ValueError('Entry Not Found')
            self.status = response.status_code
            response_info = json.loads(response.json())
            self.id = response_info['id']
            self.type_ticket = response_info['type_ticket']
            self.username = response_info['username']
            self.against_username = response_info['against_username']
            self.issue = response_info['issue']
            self.isreciept = response_info['isreciept']
            self.isresolved = response_info['isresolved']
            self.date_created = response_info['date_created']
            return 

    def is_resolved(self, isresolved : bool):
        # change status of ticket, its own function
        json_package = {
            'action' : 'isresolved',
            'id' : self.id,
            'isresolved' : isresolved
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry
    
    def update_username(self, new_username : str):
        json_package = {
            'action' : 'update_username',
            'id' : self.id,
            'update_username' : new_username
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry

    def update_against_username(self, new_against_username):
        json_package = {
            'action': 'update_against_username',
            'id' : self.id,
            'update_against_username' : new_against_username
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry
    
    def update_type(self, new_type):
        json_package = {
            'action' : 'update_type',
            'id' : self.id,
            'update_type' : new_type
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry

    def append_issue(self, issue):
        json_package = {
            'action' : 'append_issue',
            'id' : self.id,
            'append_issue' : issue
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry
    
    def update_issue(self, issue):
        json_package = {
            'action' : 'update_issue',
            'id' : self.id,
            'update_issue' : issue
        }
        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry