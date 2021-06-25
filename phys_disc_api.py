import requests, os, json

base_url = 'http://127.0.0.1:5000/api/secure/verify'
secret_token = os.environ.get('SECRET_KEY')
header_url = {'Authorization' : f'Bearer {secret_token}'}
# print(requests.get('http://127.0.0.1:5000/api/secure/verify', headers={'Authorization' : f'Bearer {secret_token}'}, params={'value1':'test'}).json())

def status_check(id : int):
    status = requests.get(base_url, headers = header_url, json = {'id' : id})

class VerifyUser():
    def __init__(self, username = None):
        if not username:
            status_check(0)
        user_status = requests.get(base_url, headers = header_url, json = {'username' : username})
        if user_status.status_code == 404:
            raise ValueError('User Not Found')
        user_info = json.loads(user_status.json())
        
        self.id = user_info['id']
        self.type_student = user_info['type_student']
        self.email = user_info['email']
        self.full_name = user_info['full_name']
        self.username = user_info['username']
        self.isreciept = user_info['isreciept']
        self.isgaucho = user_info['isgaucho']
        self.date_created = user_info['date_created']
    
    def update_gaucho(self):
        json_package = {
            'action' : 'update_gaucho',
            'username': self.username,
            'isgaucho' : True
        }
        update_user = requests.post(base_url, headers = header_url, json = json_package)
        print(update_user)

class VerificationTrigger():
    def __init__(self, user_check):
        self.user_check = user_check

    def __call__(self, *args, **kwargs):
        # if new entry is made then execute function 
        inital_length = requests.get(base_url, headers = header_url, json = {'id_len' : None}).json()
        # for index in range(1, length + 1):
        # Trying to get to the last entry and hold there till a new entry is made
        # the ids may not go in order, get list of ids then loop over that 
        index = 1 
        while True:
            gaucho_check_request = requests.get(base_url, headers = header_url, json = {'id' : index})
            gaucho_check = json.loads(gaucho_check_request.json())
            if gaucho_check['isgaucho'] == False:
                user = gaucho_check
                func = self.user_check(user, *args, **kwargs)
                return func
            else:
                current_length = requests.get(base_url, headers = header_url, json = {'id_len' : None}).json()
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
    on_submit()