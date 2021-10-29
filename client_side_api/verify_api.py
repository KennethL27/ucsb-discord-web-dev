from .setup import base_url, get_request, post_request
import json

url = base_url + 'verify'

class VerifyUser():
    def __init__(self, username = None):
        json_package = {
            'action' : 'username',
            'username' : username
        }
        user_status = get_request(json_package, url)
        if user_status.status_code == 404:
            raise ValueError('User Not Found')
        user_info = json.loads(user_status.json())
        
        self.status = user_status.status_code
        self.id = user_info['id']
        self.type_user = user_info['type_user']
        self.email = user_info['email']
        self.full_name = user_info['full_name']
        self.username = user_info['username']
        self.isreciept = user_info['isreciept']
        self.isrole = user_info['isrole']
        self.date_created = user_info['date_created']
        return
    
    def update_role(self):
        json_package = {
            'action' : 'update_role',
            'username': self.username
        }
        update_user = post_request(json_package, url)
        self.status = update_user.status_code
        return update_user
    
    def update_email(self, update_email):
        json_package = {
            'action' : 'update_email',
            'username' : self.username,
            'update_email' : update_email
        }
        update_user = post_request(json_package, url)
        self.status = update_user.status_code
        return update_user
    
    def update_name(self, update_name):
        json_package = {
            'action' : 'update_name',
            'username' : self.username,
            'name' : update_name
        }
        update_user = post_request(json_package, url)
        self.status = update_user.status_code
        return update_user

    def update_type(self, type_student):
        json_package = {
            'action' : 'update_type',
            'username' : self.username
        }
        if type_student in ['Gaucho', 'Professor', 'Physics Staff', 'Alumni' 'Visitor']:
            json_package['type'] = type_student
        else:
            raise ValueError('Not a Valid Role')

        # if type_student == 'gaucho':
        #     json_package['type'] = 'Current UCSB Student or UCSB Faculty'
        # else:
        #     json_package['type'] = 'Prospective UCSB Student'
        update_user = post_request(json_package, url)
        self.status = update_user.status_code
        return update_user