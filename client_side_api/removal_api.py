from .setup import base_url, get_request, post_request
import json

url = base_url + 'removal'

class RemovalEntry():
    def __init__(self, reasons : bool = False, usernames : bool = False, username : str = None):
        json_package = {
            'action' : None
        }

        if reasons:
            json_package['action'] = 'reasons'
            response = get_request(json_package, url)
            if response.status_code == 406:
                self.status = response['status']
                return 
            self.status = response.status_code
            self.reasons = response['reasons']
            self.other_reasons = response['other_reasons']
        
        if usernames:
            json_package['action'] = 'usernames'
            response = get_request(json_package, url)
            if response.status_code == 406:
                self.status = response['status']
                return 
            self.status = response.status_code
            self.usernames = response['useranmes']
        
        if username:
            json_package['action'] = 'username'
            json_package['username'] = username
            response = get_request(json_package, url)
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
            response = get_request(json_package, url)
            self.status = response.status_code
            self.ids = response['ids']
            return