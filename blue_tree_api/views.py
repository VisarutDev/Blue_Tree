from email.policy import default
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
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

class GetBookingByAgent(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            agent = data("agent_name") if data("agent_name") is not None else None
            voucher_code = data("voucher_code") if data("voucher_code") is not None else None
            booking_id = data("booking_id") if data("booking_id") is not None else None
            if agent != None:
                filter = Q(booking_agent_com = agent)
            elif voucher_code != None:
                filter = Q(booking_voucher_code = voucher_code)
            elif booking_id != None:
                filter = Q(booking_booking_id = booking_id)
            booking_data = UserBooking.objects.using(db_blue_tree).get(filter).jsonFormat()
            res = {
                'msg' : True,
                'data' : booking_data
            }
            return Response(res,status = status.HTTP_200_OK)
        except:
            res = {
                'msg' : False,
                'data' : 'no booking'
            }
            return Response(res,status = status.HTTP_401_UNAUTHORIZED)

class GetBookingByChoose(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            choose = data('type_choose')
            if choose == 1: #agent
                agent_code = data('agent_code')
                voucher_code = data('voucher_code')
                filter = Q(booking_agent_com = agent_code) & Q(booking_voucher_code = voucher_code)
            elif choose == 2: #gropup
                print("test222")
            elif choose == 3: #OTAs
                booking_number = data('booking_number')
                filter = Q(booking_booking_id = booking_number)
            elif choose == 4: #line
                booking_number = data('booking_number')
                filter = Q(booking_booking_id = booking_number)
            elif choose == 5: #walk in
                voucher_code = data('voucher_code')
                filter = Q(booking_voucher_code = voucher_code)
            elif choose == 6: #member
                first_name = data('first_name')
                last_name = data('last_name')
                filter = Q(booking_customer_first_name = first_name) and Q(booking_customer_last_name = last_name)
            elif choose == 7: #voucher
                voucher_code = data('voucher_code')
                filter = Q(booking_voucher_code = voucher_code)
            get_booking = UserBooking.objects.using(db_blue_tree).filter(filter).jsonFormat()
            res = {
                'msg' : True,
                'data' : get_booking
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_401_UNAUTHORIZED)

class FromForDetails(APIView):
    def get(self, request): # get draft
        try:
            data = request.GET.get
            booking = data("booking_id")
            booking_id = UserBooking.objects.using(db_blue_tree).get(booking_booking_id = booking).jsonFormat()
            try:
                info = InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = booking_id['booking_id']).values()
            except:
                info = 'no informaion'
            res = {
                'msg' : True,
                'data' : {
                    'booking' : booking_id,
                    'information' : info
                }
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request): # save draft and create detail booking
        try:
            data_guest_list = []
            data = request.data
            guests = data['guest']
            data_detail = {
                'info_detail_info_id' : data['booking_id'],
                'info_detail_country' : data['country'] if "country" in data else None,
                'info_detail_live_phuket' : data['live_in'] if "live_in" in data else None,
                'info_detail_people' : data['people'] if "people" in data else None,
                'info_detail_type_id' : data['with'] if "with" in data else None
            }
            data_booking = {
                'booking_customer_first_name' : guests[0]['first_name'],
                'booking_customer_last_name' : guests[0]['last_name'],
                'booking_age' : guests[0]['age'],
                'booking_gender' : guests[0]['gender'],
                'booking_email' : guests[0]['Email'],
                'booking_tel' : guests[0]['tel'],
                # 'booking_booking_id' : data['booking_id']
            }
            UserBooking.objects.using(db_blue_tree).filter(booking_booking_id = data['booking_id']).update_or_create(**data_booking)
            InformationDetail.objects.using(db_blue_tree).filter(info_detail_info = data['booking_id']).update_or_create(**data_detail)
            info_id = InformationDetail.objects.using(db_blue_tree).get(info_detail_info = data['booking_id'])
            del guests[0]
            if data['people'] < 10:
                for guest in guests:
                    data_list = []
                    data_list = {
                            'info_list_first_name' : guest['first_name'],
                            'info_list_last_name' : guest['last_name'],
                            'info_list_age' : guest['age'],
                            'info_list_gender' : guest['gender'],
                            'info_list_info_id' : info_id.info_detail_id
                        }
                    InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = info_id.info_detail_id,info_list_first_name = guest['first_name']).update_or_create(**data_list)
                    data_guest_list.append(data_list)
            else:
                pass

            res = {
                'msg' : True,
                'data' : {
                    'detail' : data_detail,
                    'gest_list' : data_guest_list,
                    'booking' : data_booking
                }
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            raise
            return Response(False,status=status.HTTP_401_UNAUTHORIZED)

class UpdateStatusPolicy(APIView): #api
    def put(self, request):
        try:
            data = request.data
            booking_id = data['booking_id']
            booking = InformationDetail.objects.using(db_blue_tree).filter(info_detail_info_id = booking_id).update(info_detail_status = True).values()
            user_list = InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = booking_id).update(info_list_status = True).values()
            res = {
                'msg' : True,
                'data' : {
                    'booking' : booking,
                    'user_list' : user_list
                }
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_401_UNAUTHORIZED)

class GetTypeGroup(APIView): #api
    def get(self, request):
        try:
            type = TypeGroup.objects.using(db_blue_tree).all().values()
            res = {
                'msg' : True,
                'data' : type
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False)
