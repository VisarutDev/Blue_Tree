from email.policy import default
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import *
from blue_tree.settings import db_blue_tree
import base64
from PIL import Image
from django.core.files.base import ContentFile
from io import StringIO, BytesIO
import io
from datetime import datetime

# Create your views here.
class GetBookingByAgent(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            agent = data("agent_com") if data("agent_com") is not None else None
            voucher_code = data("voucher_code") if data("voucher_code") is not None else None
            booking_id = data("booking_id") if data("booking_id") is not None else None
            customer_first_name = data("customer_first_name") if data("customer_first_name") is not None else None
            customer_last_name = data("customer_last_name") if data("customer_last_name") is not None else None
            email = data("email") if data("email") is not None else None
            booking_data = UserBooking.objects.using(db_blue_tree).filter(booking_status = 0,booking_status_policy = False)
            if booking_id != None:
                print("booking")
                booking_data = booking_data.filter(booking_booking_id = booking_id)
            if agent != None:
                print('agent')
                booking_data = booking_data.filter(booking_agent_com = agent)
            if voucher_code != None:
                print('voucher')
                booking_data = booking_data.filter(booking_voucher_code = voucher_code)
            if customer_first_name != None:
                print('first_name')
                booking_data = booking_data.filter(booking_customer_first_name = customer_first_name)
            if customer_last_name != None:
                print('last_name')
                booking_data = booking_data.filter(booking_customer_last_name = customer_last_name)
            if email != None:
                print('email')
                booking_data = booking_data.filter(booking_email = email)
            booking_data = booking_data.values()
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
            return Response(res,status = status.HTTP_400_BAD_REQUEST)

class GetBookingByChoose(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            choose = data('type_choose')
            if choose == '1': #agent
                print('agent')
                agent_code = data('agent_code')
                voucher_code = data('voucher_code')
                if voucher_code and agent_code:
                    filter = Q(booking_agent_com = agent_code) & Q(booking_voucher_code = voucher_code)
                elif agent_code:
                    filter = Q(booking_agent_com = agent_code)
                else:
                    filter = Q(booking_voucher_code = voucher_code)
            elif choose == '2': #gropup
                print('gropup')
                # pdf_64_encode = data['file']
                # format,imgstr = pdf_64_encode.split(';base64,')
                # pdf_ascii = imgstr.encode("ascii")
                # decoded = base64.decodebytes(pdf_ascii)
                # raw_pdf_io = io.BytesIO(decoded)
                # # imgstr = Image.open(raw_pdf_io)
                # img_io = io.BytesIO()
                # imgstr.save(img_io, format.split("/")[1], quality=80)
                # pdf_guest = ContentFile(img_io.getvalue(), name= str(info_id.info_detail_id) + str(datetime.utcnow()) + "." + str(format.split("/")[1]))
                # data_file = {
                #     'info_detail_file' : pdf_guest,
                #     'info_detail_file_info' : info_id.info_detail_id,
                #     'info_detail_file_booking_id' : booking
                # }
                # InformationDetailFile.objects.using(db_blue_tree).create(**data_file)
            elif choose == '3': #OTAs
                print('OTAs')
                booking_number = data('booking_number')
                filter = Q(booking_booking_id = booking_number)
            elif choose == '4': #line
                print('line')
                booking_number = data('booking_number')
                filter = Q(booking_booking_id = booking_number)
            elif choose == '5': #walk in
                print('walk in')
                voucher_code = data('voucher_code')
                filter = Q(booking_voucher_code = voucher_code)
            elif choose == '6': #member
                print('member')
                first_name = data('first_name')
                last_name = data('last_name')
                filter = Q(booking_customer_first_name = first_name) and Q(booking_customer_last_name = last_name)
            elif choose == '7': #voucher
                print('voucher')
                voucher_code = data('voucher_code')
                filter = Q(booking_voucher_code = voucher_code)
            try:
                if choose != '2':
                    print(filter)
                    get_booking = UserBooking.objects.using(db_blue_tree).filter(filter).values()
                else:
                    get_booking = 'upload success'
            except:
                get_booking = "no booking"
            res = {
                'msg' : True,
                'data' : get_booking
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request): # save draft and create detail booking
        try:
            data_guest_list = []
            data = request.data
            guests = data['guest']
            data_booking = {
                'booking_customer_first_name' : guests[0]['first_name'],
                'booking_customer_last_name' : guests[0]['last_name'] if 'last_name' in guests[0] else None,
                'booking_age' : guests[0]['age'],
                'booking_gender' : guests[0]['gender'],
                'booking_email' : guests[0]['Email'],
                'booking_tel' : guests[0]['tel'] if 'tel' in guests[0] else None,
                'booking_booking_id' : data['booking_id'] if 'booking_id' in data else None,
                'booking_voucher_code' : data['voucher_code'] if 'voucher_code' in data else None,
                'booking_agent_com' : data['agent_code'] if 'agent_code' in data else None
            }
            # booking_id, update = UserBooking.objects.using(db_blue_tree).filter(booking_booking_id = data['booking_id']).update_or_create(**data_booking)
            try:
                booking_id = UserBooking.objects.using(db_blue_tree).get(booking_booking_id = data['booking_id']).booking_id
                UserBooking.objects.using(db_blue_tree).filter(booking_booking_id = data['booking_id']).update(**data_booking)
                print("update")
            except:
                user_booking = UserBooking.objects.using(db_blue_tree).create(**data_booking)
                booking_id = user_booking.booking_id
                print("create")
            booking = booking_id
            data_detail = {
                'info_detail_info_id' : booking,
                'info_detail_country' : data['country'] if "country" in data else None,
                'info_detail_live_phuket' : data['live_in'] if "live_in" in data else None,
                'info_detail_people' : data['people'] if "people" in data else None,
                'info_detail_type' : data['with'] if "with" in data else None
            }
            info_id ,update = InformationDetail.objects.using(db_blue_tree).filter(info_detail_info = booking).update_or_create(**data_detail)
            del guests[0]

            get_info_list = InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = info_id.info_detail_id)
            print(len(get_info_list))
            print("list_id :",info_id.info_detail_id)

            if len(get_info_list) == 0:
                get_info_list = data['guest']

            type_group = TypeGroup.objects.using(db_blue_tree).get(type_group_id = data['people'])
            if type_group.type_group_file == False:
                for guest, info_list in zip(guests,get_info_list):
                    data_list = []
                    data_list = {
                            'info_list_booking_id' : booking,
                            'info_list_first_name' : guest['first_name'],
                            'info_list_last_name' : guest['last_name'],
                            'info_list_age' : guest['age'],
                            'info_list_gender' : guest['gender'],
                            'info_list_info_id' : info_id.info_detail_id
                        }
                    # InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = info_id.info_detail_id,info_list_id = info_list_id).update_or_create(**data_list)
                    try:
                        info_list_id = info_list.info_list_id
                        InformationDetailList.objects.using(db_blue_tree).filter(info_list_info_id = info_id.info_detail_id,info_list_id = info_list_id).update(**data_list)
                        print('update')
                    except:
                        InformationDetailList.objects.using(db_blue_tree).create(**data_list)
                        print('create')
                    data_guest_list.append(data_list)
            else:
                pdf_64_encode = data['file']
                format,imgstr = pdf_64_encode.split(';base64,')
                pdf_ascii = imgstr.encode("ascii")
                decoded = base64.decodebytes(pdf_ascii)
                # raw_pdf_io = io.BytesIO(decoded)
                # imgstr = Image.open(raw_pdf_io)
                imgstr = decoded
                img_io = io.BytesIO()
                imgstr.save(img_io, format.split("/")[1], quality=80)
                pdf_guest = ContentFile(img_io.getvalue(), name= str(info_id.info_detail_id) + str(datetime.utcnow()) + "." + str(format.split("/")[1]))
                data_file = {
                    'info_detail_file' : pdf_guest,
                    'info_detail_file_info' : info_id.info_detail_id,
                    'info_detail_file_booking_id' : booking
                }
                InformationDetailFile.objects.using(db_blue_tree).create(**data_file)

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
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class UpdateStatusPolicy(APIView): #api
    def put(self, request):
        try:
            data = request.data
            booking = data['booking_id']
            user_booking = UserBooking.objects.using(db_blue_tree).get(booking_booking_id = booking)
            user_booking.booking_status_policy = True
            user_booking.save()
            booking_id = user_booking.booking_id
            booking = InformationDetail.objects.using(db_blue_tree).filter(info_detail_info_id = booking_id).update(info_detail_status_policy = True).values()
            user_list = InformationDetailList.objects.using(db_blue_tree).filter(info_list_booking_id = booking_id).update(info_list_status_policy = True).values()
            InformationDetailFile.objects.using(db_blue_tree).filter(info_detail_file_booking_id = booking_id).update(info_detail_file_status_policy = True)
            res = {
                'msg' : True,
                'data' : {
                    'booking' : booking,
                    'user_list' : user_list
                }
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class GetTypeGroup(APIView):
    def get(self, request):
        try:
            collect_type = []
            data = request.GET.get
            types = TypeGroup.objects.using(db_blue_tree).all()
            if data('type_group_id'):
                try:
                    types = types.filter(type_group_id = data('type_group_id')).values()
                    collect_type = {
                        'type_group_people' : types[0]['type_group_people'],
                        'type' : types[0]
                    }
                except:
                    collect_type = "no have type_group_id"
            else :
                types_people = types.values_list('type_group_people', flat=True).distinct()
                for type in types_people:
                    types_data = types.filter(type_group_people = type).values()
                    data_type = {
                        'type_group_people' : type,
                        'type' : types_data
                    }
                    collect_type.append(data_type)
            res = {
                'msg' : True,
                'data' : collect_type
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)
