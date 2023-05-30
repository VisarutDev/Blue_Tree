from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from blue_tree.settings import db_blue_tree
from .utils import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token, Hash

# Create your views here.
class CreateToken(APIView):
    def get(self, request):
        access_token = create_access_token(2)
        refresh_token = create_refresh_token(2)
        res = {
            "msg" : True,
            "token" : access_token
        }

        response = Response()
        response.set_cookie(key = 'refreshToken',value =refresh_token, httponly=True)
        response.data = {
            'token' : res
        }
        return response
class RefreshTokenAPI(APIView):
    def post(self, request):
        refresh_token = verify_refresh_token(request)
        access_token = create_access_token(refresh_token)
        res = {
            'access_token' : access_token
        }
        return Response(res)

class UserTestRefreshToken(APIView):
    def get(self, request):
        payload = verify_access_token(request)
        if payload != False:
            res = "success"
        else :
            res = "false"
        return Response(res)

class Register(APIView):
    def post(self, request):
        data = request.data
        print(data)
        password = Hash.hash_password(data['password'])
        check = Hash.check_password(password,data['password'])
        res = {
            "pass_word" : password,
            "check_pass" : check
        }
        return Response(res)

class Apicheck(APIView):
    def get(self, request):
        payload = verify_access_token(request)
        if payload != False:
            data = request.data
            return Response(data)
        else:
            return Response(False)