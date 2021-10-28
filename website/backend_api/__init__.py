from .. import api, auth
from flask import request
from .verify import Verify_API
from .ticket import Ticket_API
from .removal import Removal_API
from .emoji import Emoji_API
import os

secret_token = os.environ.get('SECRET_KEY')
TOKEN = {
    'token' : secret_token
}

@auth.verify_token
def verify_token(token):
    if token in TOKEN['token']:
        return token

api.add_resource(Verify_API, '/verify')
api.add_resource(Ticket_API, '/ticket')
api.add_resource(Removal_API, '/removal')
api.add_resource(Emoji_API, '/emoji')