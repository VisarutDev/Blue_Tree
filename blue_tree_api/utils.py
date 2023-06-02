from base64 import decode
from os import access
import jwt
from datetime import datetime, timedelta
import hashlib
import uuid
key = uuid.uuid4().hex

#config jwt token
JWT_SECRET = 'secret'
JWT_REFRESH = 'refresh_secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120
JWT_EXP_DELTA_SECONDS_REFRESH = 1800

db_blue_tree = 'db_blue_tree'
def create_access_token(user):
    payload = {
        'user_id': user,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    token = jwt_token.decode('utf-8')
    return token

def create_refresh_token(user):
    payload = {
        'user_id': user,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS_REFRESH)
    }
    jwt_token = jwt.encode(payload, JWT_REFRESH, JWT_ALGORITHM)
    token = jwt_token.decode('utf-8')
    return token

def verify_access_token(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        access_token = request.META['HTTP_AUTHORIZATION']
        try:
            check_token = []
            res = 'msg_token_invalid'
            payload = jwt.decode(access_token, JWT_SECRET, algorithms= JWT_ALGORITHM)
            # check_token = Token.objects.using(db_blue_tree).filter(user_id = payload['user_id']).values()
            for check in check_token:
                if access_token == check.access_token:
                    res = {
                        'status' : True,
                        'user_id' : check.user_id
                    }
                    break
            return payload['user_id']
        except:
            res = False
            return res

def verify_refresh_token(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        refresh_token = request.META['HTTP_AUTHORIZATION']
        try:
            check_token = []
            # res = 'msg_token_invalid'
            payload = jwt.decode(refresh_token, JWT_SECRET, JWT_ALGORITHM)
            # check_token = Token.objects.using(db_blue_tree).filter(user_id = payload['user_id']).values()
            for check in check_token:
                if refresh_token == check.access_token:
                    res = {
                        'status' : True,
                        'user_id' : check.user_id
                    }
                    break
            id = payload['user_id']
            return id
        except:
            res = 'msg_token_invalid'
            return res

class Hash():
    def hash_password(password):
        hash_password = hashlib.sha256(key.encode() + password.encode()).hexdigest() + ':' + key
        return hash_password

    def check_password(hashed_password, user_password):
        password, hashed = hashed_password.split(':')
        return password == hashlib.sha256(hashed.encode() + user_password.encode()).hexdigest()