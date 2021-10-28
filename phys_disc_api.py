import re
import requests, os, json

from requests.api import delete, get

base_url = 'http://127.0.0.1:5000/api/secure/verify'
secret_token = os.environ.get('SECRET_KEY')
header_url = {'Authorization' : f'Bearer {secret_token}'}

def get_request(json_package):
    response = requests.get(base_url, headers = header_url, json = json_package)
    return response

def post_request(json_package):
    response = requests.post(base_url, headers = header_url, json = json_package)
    return response

# Verify Table API
class VerifyUser():
    def __init__(self, username = None):
        json_package = {
            'action' : 'username',
            'username' : username
        }
        user_status = get_request(json_package)
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
        update_user = post_request(json_package)
        self.status = update_user.status_code
        return update_user
    
    def update_email(self, update_email):
        json_package = {
            'action' : 'update_email',
            'username' : self.username,
            'update_email' : update_email
        }
        update_user = post_request(json_package)
        self.status = update_user.status_code
        return update_user
    
    def update_name(self, update_name):
        json_package = {
            'action' : 'update_name',
            'username' : self.username,
            'name' : update_name
        }
        update_user = post_request(json_package)
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
        update_user = post_request(json_package)
        self.status = update_user.status_code
        return update_user

class TicketEntry():
    def __init__(self, id : int = None, unresolved : bool = False ):
        json_package = {
            'action' : None,
            'id' : None
        }

        # get all unresolved entries
        if unresolved:
            json_package['action'] = 'unresolved'
            response = get_request(json_package).json()
            self.ids = response['unresolved_ids']
            self.status = response.status_code
            return

        # Getting all entry ids if no id is given
        if not id:
            response = get_request(json_package).json()
            self.ids = response['ids']
            self.status = response.status_code
            return 

        # view ticket        
        else:
            json_package['action'] = 'id'
            json_package['id'] = id
            response = get_request(json_package)
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
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry
    
    def update_username(self, new_username : str):
        json_package = {
            'action' : 'update_username',
            'id' : self.id,
            'update_username' : new_username
        }
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry

    def update_against_username(self, new_against_username):
        json_package = {
            'action': 'update_against_username',
            'id' : self.id,
            'update_against_username' : new_against_username
        }
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry
    
    def update_type(self, new_type):
        json_package = {
            'action' : 'update_type',
            'id' : self.id,
            'update_type' : new_type
        }
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry

    def append_issue(self, issue):
        json_package = {
            'action' : 'append_issue',
            'id' : self.id,
            'append_issue' : issue
        }
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry
    
    def update_issue(self, issue):
        json_package = {
            'action' : 'update_issue',
            'id' : self.id,
            'update_issue' : issue
        }
        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry

class RemovalEntry():
    def __init__(self, reasons : bool = False, usernames : bool = False, username : str = None):
        json_package = {
            'action' : None
        }

        if reasons:
            json_package['action'] = 'reasons'
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response['status']
                return 
            self.status = response.status_code
            self.reasons = response['reasons']
            self.other_reasons = response['other_reasons']
        
        if usernames:
            json_package['action'] = 'usernames'
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response['status']
                return 
            self.status = response.status_code
            self.usernames = response['useranmes']
        
        if username:
            json_package['action'] = 'username'
            json_package['username'] = username
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response['status']
                return
            self.status = response.status_code
            response_info = json.loads(response.json())
            self.id = response_info['id']
            self.reason = response_info['reason']
            self.other_reason = response_info['other_reason']
            self.email = response_info['email']
            self.username = response_info['username']
            self.comments = response_info['comments']
            self.isreciept = response_info['isreciept']
            self.date_created = response_info['date_created']

        else:
            json_package['action'] = 'ids'
            response = get_request(json_package)
            self.status = response.status_code
            self.ids = response['ids']
            return
        
class EmojiEntry():
    def __init__(self, id : int = None, inserver : bool = None):
        json_package = {
            'action' : None
        }

        if id:
            json_package['action'] = 'id'
            json_package['id'] = id
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response['status']
                return
            self.status = response.status_code
            response_info = json.loads(response.json())
            self.id = response_info['id']
            self.username = response_info['username']
            self.description = response_info['description']
            # going to need to handle this differently
            self.emoji_image = response_info['emoji_image']
            self.emoji_image_name = response_info['emoji_image_name']
            self.emoji_image_type = response_info['emoji_image_type']
            self.date_created = response_info['date_created']
            return
        
        if inserver in [False, True]:
            json_package['action'] = 'inserver'
            json_package['inserver'] = inserver
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response.json()['status']
                return
            self.status = response.status_code
            self.inserver_ids = response.json()['inserver_ids']
            return

        else:
            json_package['action'] = 'ids'
            response = get_request(json_package)
            if response.status_code == 406:
                self.status = response.json()['status']
                return
            self.status = response.status_code
            self.ids = response.json()['ids']
            return
    
    def update_inserver(self, isinserver : bool):
        json_package = {
            'action' : 'isinserver',
            'id' : self.id,
            'isinserver' : isinserver
        }

        update_entry = post_request(json_package)
        self.status = update_entry.status_code
        return update_entry

    def delete_entry(self):
        json_package = {
            'action' : 'delete_entry',
            'id' : self.id
        }

        delete_entry = post_request(json_package)
        self.status = delete_entry.status_code
        return delete_entry

class VerificationTrigger():
    def __init__(self, user_check):
        self.user_check = user_check

    def __call__(self, *args, **kwargs):
        # if new entry is made then execute function 
        json_package_1 = {
            'action' : 'id_len'
        }
        inital_length = get_request(json_package_1).json()
        # for index in range(1, length + 1):
        # Trying to get to the last entry and hold there till a new entry is made
        # the ids may not go in order, get list of ids then loop over that 
        json_package_2 = {
            'action' : 'id'
        }
        index = 1 
        while True:
            json_package_2['id'] = index
            gaucho_check_request = get_request(json_package_2)
            gaucho_check = json.loads(gaucho_check_request.json())
            if gaucho_check['isgaucho'] == False:
                user = gaucho_check
                func = self.user_check(user, *args, **kwargs)
                return func
            else:
                current_length = get_request(json_package_1).json()
                if inital_length < current_length:
                    index += 1
                    continue
            
            # try:
            #     gaucho_check = json.loads(gaucho_check_request.json())
            #     if gaucho_check['isgaucho'] == False:
            #         user = gaucho_check
            #         func = self.user_check(user, *args, **kwargs)
            #     else:
            #         index += 1
            # except:
            #     return func
        # if no new entry is made then hold off on executing the function
        
@VerificationTrigger
def on_submit(user): # user variable should contain the information that was submitted when form was filled out
    # using discord api and provided user's username give the user's username the role
    # then update user on the db using website api
    VerifyUser(user['username']).update_gaucho()

if __name__ == '__main__':
    status = VerifyUser()
    # status.update_type('Gaucho')
    # status.update_role()
    # # print(status)
    # # status = TicketEntry(1).update_issue('this did not work')
    # # status = TicketEntry(id = 1).is_resolved(True)
    # # status = RemovalEntry(username='test#1234')
    # # print(status.isreciept)
    # status = EmojiEntry(id = 1)
    print(status)