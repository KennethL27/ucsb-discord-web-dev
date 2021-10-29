import requests, os

base_url = 'http://127.0.0.1:5000/api/secure/'
secret_token = os.environ.get('SECRET_KEY')
header_url = {'Authorization' : f'Bearer {secret_token}'}

def get_request(json_package, url):
    response = requests.get(url, headers = header_url, json = json_package)
    return response

def post_request(json_package, url):
    response = requests.post(url, headers = header_url, json = json_package)
    return response
