from .setup import base_url, get_request, post_request
import json

url = base_url + 'emoji'

class EmojiEntry():
    def __init__(self, id : int = None, inserver : bool = None):
        json_package = {
            'action' : None
        }

        if id:
            json_package['action'] = 'id'
            json_package['id'] = id
            response = get_request(json_package, url)
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
            response = get_request(json_package, url)
            if response.status_code == 406:
                self.status = response.json()['status']
                return
            self.status = response.status_code
            self.inserver_ids = response.json()['inserver_ids']
            return

        else:
            json_package['action'] = 'ids'
            response = get_request(json_package, url)
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

        update_entry = post_request(json_package, url)
        self.status = update_entry.status_code
        return update_entry

    def delete_entry(self):
        json_package = {
            'action' : 'delete_entry',
            'id' : self.id
        }

        delete_entry = post_request(json_package, url)
        self.status = delete_entry.status_code
        return delete_entry