from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import verify_access_token, verify_refresh_token, Hash, send_email_approve_register, set_data_send_email, CreateTokenUser
from blue_tree_bof.models import BannerApp, HappeningApp, NotificationApp, PromotionApp, ServiceApp, Users, UsersToken, NotificationApp
from blue_tree.settings import db_blue_tree
url_bucket = ''
class RefreshTokenAPI(APIView):
    def post(self, request):
        try:
            refresh = request.data
            check_refresh_token = verify_refresh_token(refresh['refreshToken'])
            if check_refresh_token['status'] == False:
                return Response(check_refresh_token['data'],status=status.HTTP_404_NOT_FOUND)

            create = CreateTokenUser(check_refresh_token['user_id'],1)
            res = {
                'msg' : True,
                'access_token' : create['token'],
                'refresh_token' : create['refreshToken']
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    def post(self, request):
        try:
            data = request.data
            try:
                Users.objects.using(db_blue_tree).get(users_email = data['users_email'])
                res = {
                    'msg' : False,
                    'data' : 'This email is already in use.'
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            users_password = Hash.hash_password(data['users_password'])
            data_users = {
                'users_email' : data['users_email'],
                'users_password' : users_password,
            }
            Users.objects.using(db_blue_tree).create(**data_users)
            data_users['type_send_mail'] = 1
            data_users = set_data_send_email(data_users)
            print(data_users)
            # send_email_approve_register(data_users)
            res = {
                'msg' : True,
                'data' : data_users
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class LoginApp(APIView):
    def post(self, request):
        try:
            data = request.data
            get_users = Users.objects.using(db_blue_tree).get(users_email = data['users_email'])
            if get_users.users_verify == 1 and get_users.users_status == 1:
                check = Hash.check_password(get_users.users_password,data['users_password'])
                if check:
                # if True:
                    try:
                        print("Login")
                        token = UsersToken.objects.using(db_blue_tree).get(users_token_users_id = get_users.users_id)
                        request.META['HTTP_AUTHORIZATION'] = token.users_token_key
                        payload = verify_access_token(request)
                        if payload['status'] == True:
                            get_users.users_activate_at = datetime.now()
                            get_users.save()
                            data_user = {
                                'users_id' : get_users.users_id,
                                'access_token' : token.users_token_key
                            }
                        else:
                            get_users.users_activate_at = datetime.now()
                            get_users.save()
                            users_id = get_users.users_id
                            create = CreateTokenUser(users_id,1)
                            data_user = {
                                'users_id' : users_id,
                                'access_token' : create['token'],
                                'refresh_Token' : create['refreshToken']
                            }
                        res = {
                            'msg' : True,
                            'data' : data_user
                        }
                        response = Response(res, status=status.HTTP_200_OK)
                    except: #first login
                        print("First login")
                        users_id = get_users.users_id
                        create = CreateTokenUser(users_id)
                        data_user = {
                            'users_id' : users_id,
                            'access_token' : create['token'],
                            'refresh_Token' : create['refreshToken']
                        }
                        res = {
                            'msg' : True,
                            'data' : data_user
                        }
                        response = Response(res,status = status.HTTP_200_OK)
                        # response.set_cookie(key = 'refreshToken',value =create['refreshToken'], httponly=True)
                else:
                    res = {
                        'msg' : False,
                        'data' : "password is incorrect"
                    }
                    response = Response(res, status=status.HTTP_200_OK)
            else:
                res = {
                    'msg' : True,
                    'data' : 'You must verify your identity by email.'
                }
                response = Response(res, status=status.HTTP_200_OK)
            return response
        except:
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)

class ForgetPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            users_password = Hash.hash_password(data['users_password'])
            users = Users.objects.using(db_blue_tree).filter(users_email = data['users_email'])
            data_users = {
                'users_status' : 0,
                'users_password' : users_password
            }
            users.update(**data_users)
            data_users['type_send_mail'] = 2
            data_users['users_email'] = data['users_email']
            data_users = set_data_send_email(data_users)
            # send_email_approve_register(data_users)
            res = {
                'msg' : True,
                'data' : data_users
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEmail(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            users = Users.objects.using(db_blue_tree).get(users_id = data('user_id'))
            users.users_verify = 1
            users.users_status = 1
            users.save()
            res = {
                'msg' : True,
                'data' : data('user_id')
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)

class GetBannerHomePage(APIView):
    def get(self, request):
        try:
            payload = verify_access_token(request)
            if payload['status'] == False:
                return Response(payload,status=status.HTTP_401_UNAUTHORIZED)

            banners = BannerApp.objects.using(db_blue_tree).filter(banner_status = 1, delete_at = None)
            if request.GET.get('banner_id'):
                banners = banners.filter(banner_id = request.GET.get('banner_id')).values()
                banners[0]['banner_image'] = str(url_bucket) + str(banners[0]['banner_image'])
                banners = banners[0]
            else:
                for banner in banners:
                    banner.banner_image = str(url_bucket) + str(banner.banner_image)
                banners = banners.values()
            res = {
                'msg' : True,
                'data' : banners
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetPromotionHomePage(APIView):
    def get(self, request):
        try:
            payload = verify_access_token(request)
            if payload['status'] == False:
                return Response(payload,status=status.HTTP_401_UNAUTHORIZED)

            promotions = PromotionApp.objects.using(db_blue_tree).filter(promotion_status = 1, delete_at = None)
            if request.GET.get('promotion_id'):
                promotions = promotions.filter(promotion_id = request.GET.get('promotion_id')).values()
                promotions[0]['promotion_image'] = str(url_bucket) + str(promotions[0]['promotion_image'])
                promotions = promotions[0]
            else:
                for promotion in promotions:
                    promotion.promotion_image = str(url_bucket) + str(promotion.promotion_image)
                promotions = promotions.values()
            res = {
                'msg' : True,
                'data' : promotions
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetServiceHomePage(APIView):
    def get(self, request):
        try:
            payload = verify_access_token(request)
            if payload['status'] == False:
                return Response(payload,status=status.HTTP_401_UNAUTHORIZED)

            services = ServiceApp.objects.using(db_blue_tree).filter(service_status = 1, delete_at = None)
            if request.GET.get('service_id'):
                services = services.filter(service_id = request.GET.get('service_id')).values()
                services[0]['service_icon'] = str(url_bucket) + str(services[0]['service_icon'])
                services = services[0]
            else:
                for service in services:
                    service.service_icon = str(url_bucket) + str(service.service_icon)
                services = services.values()
            res = {
                'msg' : True,
                'data' : services
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetHappeningHomePage(APIView):
    def get(self, request):
        try:
            payload = verify_access_token(request)
            if payload['status'] == False:
                return Response(payload,status=status.HTTP_401_UNAUTHORIZED)

            happenings = HappeningApp.objects.using(db_blue_tree).filter(happening_status = 1, delete_at = None)
            if request.GET.get('happening_id'):
                happenings = happenings.filter(happening_id = request.GET.get('happening_id')).values()
                happenings[0]['happening_image'] = str(url_bucket) + str(happenings[0]['happening_image'])
                happenings = happenings[0]
            else:
                for happening in happenings:
                    happening.happening_image = str(url_bucket) + str(happening.happening_image)
                happenings = happenings.values()
            res = {
                'msg' : True,
                'data' : happenings
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetNotificationHomePage(APIView):
    def get(self, request):
        try:
            payload = verify_access_token(request)
            if payload['status'] == False:
                return Response(payload,status=status.HTTP_401_UNAUTHORIZED)

            get_noti = NotificationApp.objects.using(db_blue_tree).filter(notification_status = 1, delete_at = None)
            if request.GET.get('notification_id'):
                get_noti = get_noti.filter(notification_id = request.GET.get('notification_id')).values()
                get_noti[0]['notification_image'] = str(url_bucket) + str(get_noti[0]['notification_image'])
                get_noti = get_noti[0]
            else:
                for noti in get_noti:
                    noti.notification_image = str(url_bucket) + str(noti.notification_image)
                get_noti = get_noti.values()
            res = {
                'msg' : True,
                'data' : get_noti
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetInformation(APIView):
    def get(self, request):
        payload = verify_access_token(request)
        if payload['status'] == False:
            return Response(payload,status=status.HTTP_401_UNAUTHORIZED)
        try:
            get_user = Users.objects.using(db_blue_tree).filter(users_id = payload['user_id']).values()
            get_user[0]['users_image'] = str(get_user[0]['users_image'])
            res = {
                'msg' : True,
                'data' : get_user[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class Apicheck(APIView):
    def get(self, request):
        payload = verify_access_token(request)
        if payload != False:
            data = request.data
            return Response(data)
        else:
            return Response(False)

class Test(APIView):
    def get(self,request):
        data = request.GET.get
        user_name = data('users_email').replace('@',' ').split()
        print(user_name)
        return Response(user_name[0],status = status.HTTP_200_OK)