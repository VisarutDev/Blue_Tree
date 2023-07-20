import imp
from blue_tree_bof.models import UsersToken
import jwt
from datetime import datetime, timedelta
import hashlib
import uuid
key = uuid.uuid4().hex
from django.template import loader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, To, Email, Subject, HtmlContent, Mail, Content, FileContent, Attachment, FileName, FileType, Disposition, ContentId
from blue_tree_bof.models import UsersToken
import base64
from rest_framework.response import Response
from blue_tree.settings import db_blue_tree

#config jwt token
JWT_SECRET = 'secret'
JWT_REFRESH = 'refresh_secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 300
# JWT_EXP_DELTA_SECONDS_REFRESH = 18000000
JWT_EXP_DELTA_SECONDS_REFRESH = 1

sendgrid_key = ''
primary_email = ''


def CreateTokenUser(users_id,type = 0):
    access_token = create_access_token(users_id)
    refresh_token = create_refresh_token(users_id)
    data = {
        'users_token_key' : access_token,
        'users_token_users_id' : users_id,
        'users_token_refresh' : refresh_token
    }
    if type == 0:
        UsersToken.objects.using(db_blue_tree).create(**data)
    else:
        UsersToken.objects.using(db_blue_tree).filter(users_token_users_id = users_id).update(**data)
    res = {
        "msg" : True,
        "token" : access_token,
        "refreshToken" : refresh_token
    }
    return res

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
        'exp': datetime.utcnow() + timedelta(days=JWT_EXP_DELTA_SECONDS_REFRESH)
    }
    jwt_token = jwt.encode(payload, JWT_REFRESH, JWT_ALGORITHM)
    token = jwt_token.decode('utf-8')
    return token

def verify_access_token(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        access_token = request.META['HTTP_AUTHORIZATION']
        try:
            check_token = []
            payload = jwt.decode(access_token, JWT_SECRET, algorithms= JWT_ALGORITHM)
            check_token = UsersToken.objects.using(db_blue_tree).filter(users_token_users_id = payload['user_id'])
            for check in check_token:
                if access_token == check.users_token_key:
                    res = {
                        'status' : True,
                        'user_id' : check.users_token_users_id
                    }
                    break
                else:
                    res = {
                        'status' : False,
                        'data' : 'msg_token_invalid'
                    }
            return res
        except:
            res = {
                'status' : False,
                'data' : "Signature has expired"
            }
            return res

def verify_refresh_token(data):
    if data:
        refresh_token = data
        try:
            try:
                check_token = UsersToken.objects.using(db_blue_tree).get(users_token_refresh = refresh_token)
            except:
                res = {
                    'status' : False,
                    'data' : 'refresh_token_mismatch',
                }
                return res

            payload = jwt.decode(refresh_token, JWT_REFRESH, JWT_ALGORITHM)
            if refresh_token == check_token.users_token_refresh:
                res = {
                    'status' : True,
                    'user_id' : payload['user_id']
                }
            return res
        except jwt.ExpiredSignatureError as identifier:
            payload = jwt.decode(refresh_token, JWT_REFRESH, JWT_ALGORITHM, options={'verify_exp':False})
            res = {
                'status' : True,
                'data' : 'refresh_token_invalid',
                'user_id' : payload['user_id']
            }
            return res

class Hash():
    def hash_password(password):
        hash_password = hashlib.sha256(key.encode() + password.encode()).hexdigest() + ':' + key
        return hash_password

    def check_password(hashed_password, user_password):
        password, hashed = hashed_password.split(':')
        return password == hashlib.sha256(hashed.encode() + user_password.encode()).hexdigest()

def set_data_send_email(data):
    if data['type_send_mail'] == 1:
        type_send = "approve_register"
    elif data['type_send_mail'] == 2:
        type_send = "forget_password"
    print(type_send)
    user_name = data['users_email'].replace('@',' ').split()
    user_name = user_name[0]
    data_users = {
            'email' : data['users_email'],
            'users_password' : data['users_password'],
            'user_name' : user_name,
            'type_send_mail' : type_send
        }
    return data_users

def send_email_approve_register(data):
    if data["type_send_mail"]=="approve_register":
        template = loader.get_template('approve_register.html')
        data_email = {  "user_name":data["user_name"],
                        "email" : data["email"]}

    elif data["type_send_mail"]=="forget_password":
        template = loader.get_template('forget_password.html')
        data_email = {  "user_name":data["user_name"],
                        "email" : data["email"]}
    print(data_email)
    html = template.render(data_email)
    from_email = From(primary_email)
    to_email = To(data["email"])
    subject = Subject("Blue Tree : ยืนยันตัวตนการลงทะเบียน")
    html_content = HtmlContent(html)
    message = Mail(from_email, to_email, subject, html_content)
    body = """
            """+html+"""
            """
    try:
        sendgrid_client = SendGridAPIClient(sendgrid_key)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print("success")
        return True
    except Exception as error:
        print("Error sent mail : ", error)
        raise
        return False