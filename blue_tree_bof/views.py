from datetime import datetime
from venv import create
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from blue_tree.settings import db_blue_tree
from .utils import generate_booking, UploadImage
# import io
# import base64
# from PIL import Image
# from django.core.files.base import ContentFile
from django.db.models import Q

url_bucket = ''

# class GetFillType(APIView):
#     def get(self):
#         try:
#             fill = FillType.objects.using(db_blue_tree).filter(fill_type_status = 1).values()
#             res = {
#                 'msg' : True,
#                 'data' : fill
#             }
#             return Response(res,status=status.HTTP_200_OK)
#         except:
#             return Response({'msg':False},status=status.HTTP_401_UNAUTHORIZED)

class ManageFillList(APIView):
    def get(self, request): #get all fill list
        try:
            fill_list = []
            data = request.GET.get
            page_size = int(data("page_size"))
            current_page = int(data("current_page"))
            get_fills = FillList.objects.using(db_blue_tree).filter(delete_at = None, fill_status = 1)

            if data("search"):
                search = data("search")
                get_fills = get_fills.filter(Q(fill_name = search) or Q(fill_type = search))

            for fill in get_fills:
                get_sub_fill = SubFillList.objects.using(db_blue_tree).filter(sub_fill_list_id = fill.fill_id, delete_at = None).count()
                data_list = {
                    'fill_id' : fill.fill_id,
                    'fill_name' : fill.fill_name,
                    'fill_type' : fill.fill_type,
                    'fill_status' : fill.fill_status,
                    'sub_fill_count' : get_sub_fill if get_sub_fill != 0 else "-"
                }
                fill_list.append(data_list)
            res = {
                'msg' : True,
                'data' : fill_list[page_size * (current_page-1) : page_size * current_page]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            fill_id = data['fill_id']
            fill_name = data['fill_name']
            fill_type = data['fill_type']
            fill_list = FillList.objects.using(db_blue_tree).filter(fill_id = fill_id)
            data_fill = {
                'fill_name' : fill_name,
                'fill_type' : fill_type
            }
            fill_list.update(**data_fill)
            data_fill['fill_id'] = fill_id
            res = {
                'msg' : True,
                'data' : data_fill
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            fill_name = data['fill_name']
            fill_type = data['fill_type']
            data_fill = {
                "fill_name" : fill_name,
                "fill_type" : fill_type
            }
            get_fill, create = FillList.objects.using(db_blue_tree).get_or_create(**data_fill)
            data_fill['fill_id'] = get_fill.fill_id
            res = {
                'msg' : True,
                'data' : data_fill
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            fill_id = data['fill_id']
            fill_list = FillList.objects.using(db_blue_tree).get(fill_id = fill_id)
            fill_list.delete_at = date_time
            fill_list.fill_status = 2
            fill_list.save()
            res = {
                'msg' : True,
                'data' : fill_id
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class ManageSubFillList(APIView):
    def get(self,request): # get sub fill all by fill list id
        try:
            data = request.GET.get
            page_size = int(data("page_size"))
            current_page = int(data("current_page"))
            sub_fill_list_id = data('fill_list_id')
            get_sub_fill = SubFillList.objects.using(db_blue_tree).filter(sub_fill_list_id = sub_fill_list_id, delete_at = None, sub_fill_status__in = [0,1]).values()

            if data("search"):
                search = data('search')
                get_sub_fill = get_sub_fill.filter(sub_fill_name = search)

            res = {
                'msg' : True,
                'data' : get_sub_fill[page_size * (current_page-1) : page_size * current_page]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        try:
            data = request.data
            sub_fill_id = data['sub_fill_id']
            sub_fill_name = data['sub_fill_name']
            sub_fill_list = data['sub_fill_list_id']
            sub_fill_status = data['sub_fill_status']
            sub_fill_description = data['sub_fill_description']
            sub_fill = SubFillList.objects.using(db_blue_tree).filter(sub_fill_id = sub_fill_id)
            data_sub_fill = {
                'sub_fill_name' : sub_fill_name,
                'sub_fill_list_id' : sub_fill_list,
                'sub_fill_status' : sub_fill_status,
                'sub_fill_description' : sub_fill_description
            }
            sub_fill.update(**data_sub_fill)
            data_sub_fill['sub_fill_id'] = sub_fill_id
            res = {
                'msg' : True,
                'data' : data_sub_fill
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            data = request.data
            sub_fill_name = data['sub_fill_name']
            sub_fill_list = data['sub_fill_list_id']
            sub_fill_description = data['sub_fill_description'] if 'sub_fill_description' in data else None
            data_sub_fill = {
                'sub_fill_name' : sub_fill_name,
                'sub_fill_list_id' : sub_fill_list,
                'sub_fill_description' : sub_fill_description
            }
            get_sub, create = SubFillList.objects.using(db_blue_tree).get_or_create(**data_sub_fill)
            data_sub_fill['sub_fill_id'] = get_sub.sub_fill_id
            res = {
                'msg' : True,
                'data' : data_sub_fill
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            sub_fill_id = data['sub_fill_id']
            sub_fill = SubFillList.objects.using(db_blue_tree).get(sub_fill_id = sub_fill_id)
            sub_fill.delete_at = date_time
            sub_fill.sub_fill_status = 2
            sub_fill.save()
            res = {
                'msg' : True,
                'data' : sub_fill_id
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class GetFillListAndSubFill(APIView): #get fill list all and sub fill all for create order
    def get(self, request):
        try:
            get_fills = FillList.objects.using(db_blue_tree).filter(fill_status = 1).values()
            for index, fill_list in enumerate(get_fills):
                data_sub_fill = []
                get_sub_fills = SubFillList.objects.using(db_blue_tree).filter(sub_fill_list_id = fill_list['fill_id'], delete_at = None, sub_fill_status = 1).values()
                for sub_fill in get_sub_fills:
                    data_sub_fill.append(sub_fill)
                get_fills[index]['sub_fill'] = data_sub_fill
            res = {
                'msg' : True,
                'data' : get_fills
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class ManageOrderBof(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            page_size = int(data('page_size'))
            current_page = int(data('current_page'))
            orders = Order.objects.using(db_blue_tree).filter(order_status_policy = False, order_status = 0, delete_at = None).values()
            channels = ChannelType.objects.using(db_blue_tree).all()

            if data("search"):
                search = data('search')
                orders = orders.filter(Q(order_booking_id = search) or Q(order_customer_name = search))

            for index,order in enumerate(orders):
                channels = channels.filter(channel_type_id = order['order_channel_id']).values()
                image = url_bucket + str(order['order_payment_slip'])
                orders[index]['order_payment_slip'] = image
                orders[index]['order_channel_id'] = channels[0]
            res = {
                'msg' : True,
                'data' : orders[page_size * (current_page - 1) : page_size * current_page]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            date_time = (datetime.now()).strftime("%Y%m%d%H%M%S")
            orders = Order.objects.using(db_blue_tree).filter(order_booking_id = data['order_booking_id'])
            channel = ChannelType.objects.using(db_blue_tree).filter(channel_type_id = orders[0].order_channel_id).values()

            try:
                data['image_slip']
                get_image = Order.objects.using(db_blue_tree).get(order_booking_id = data['order_booking_id'])
                image_slip = data['image_slip']
                # image_64_encode = image_slip
                # format, imgstr = image_64_encode.split(';base64,')
                # image_ascii = imgstr.encode("ascii")
                # decoded = base64.decodebytes(image_ascii)
                # raw_img_io = io.BytesIO(decoded)
                # imgstr = Image.open(raw_img_io)
                # # imgstr = imgstr.resize((480, 320))
                # img_io = io.BytesIO()
                # imgstr.save(img_io, format.split("/")[1], quality=80)

                # image_slip = ContentFile(img_io.getvalue(),name= str(channel.channel_code) +"_"+str(date_time)+"."+str(format.split("/")[1]))
                name = str(channel[0]['channel_code']) + "_" + str(date_time)
                image_slip = UploadImage(image_slip,name)
                get_image.order_payment_slip = image_slip
                get_image.save()
            except:
                image_slip = Order.objects.using(db_blue_tree).get(order_booking_id = data['order_booking_id']).order_payment_slip

            data_booking = {
                'order_id_order_agent' : data['id_order_agent'],
                'order_agent_name' : data['agent_name'],
                'order_booking_date' : data['booking_date'],
                'order_use_date' : data['use_date'],
                'order_customer_name' : data['customer_name'],
                'order_mobile_phone' : data['mobile_phone'],
                'order_email' : data['email'],
                'order_number_of_people' : data['number_of_people'],
                'order_credit_term' : data['credit_term'],
                'order_comment' : data['order_comment'],
                'order_information' : data['order_information'],
                'order_customer_fill' : data['customer_fill']
            }
            orders.update(**data_booking)
            data_booking['order_payment_slip'] = str(image_slip)
            data_booking['order_channel_id'] = channel[0]
            data_booking['order_booking_id'] = orders[0].order_booking_id
            res = {
                'msg' : True,
                'data' : data_booking
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            channel_id = int(data['channel'])
            booking_code = data['booking_code']
            channel = ChannelType.objects.using(db_blue_tree).get(channel_type_id = channel_id)
            # booking_code = generate_booking(channel.channel_code)
            date_time = (datetime.now()).strftime("%Y%m%d%H%M%S")
            try:
                image_slip = data['image_slip']
                # image_64_encode = image_slip
                # format, imgstr = image_64_encode.split(';base64,')
                # image_ascii = imgstr.encode("ascii")
                # decoded = base64.decodebytes(image_ascii)
                # raw_img_io = io.BytesIO(decoded)
                # imgstr = Image.open(raw_img_io)
                # # imgstr = imgstr.resize((480, 320))
                # img_io = io.BytesIO()
                # imgstr.save(img_io, format.split("/")[1], quality=80)

                # image_slip = ContentFile(img_io.getvalue(),name= str(channel.channel_code) +"_"+str(date_time)+"."+str(format.split("/")[1]))
                name = str(channel.channel_code) + "_" + str(date_time)
                image_slip = UploadImage(image_slip,name)

            except:
                image_slip = None

            data_booking = {
                'order_channel_id' : channel_id,
                'order_booking_id' : booking_code,
                'order_id_order_agent' : data['id_order_agent'],
                'order_agent_name' : data['agent_name'],
                'order_booking_date' : data['booking_date'],
                'order_use_date' : data['use_date'],
                'order_customer_name' : data['customer_name'],
                'order_mobile_phone' : data['mobile_phone'],
                'order_email' : data['email'],
                'order_number_of_people' : data['number_of_people'],
                'order_credit_term' : data['credit_term'],
                'order_payment_slip' : image_slip,
                'order_comment' : data['order_comment'],
                'order_information' : data['order_information'],
                'order_customer_fill' : data['customer_fill']
            }
            Order.objects.using(db_blue_tree).create(**data_booking)
            data_booking['order_payment_slip'] = str(image_slip)
            res = {
                'msg' : True,
                'data' : data_booking
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            booking_id = data['booking_id']
            order = Order.objects.using(db_blue_tree).get(order_booking_id = booking_id)
            order.order_status = 2
            order.delete_at = date_time
            order.save()
            res = {
                'msg' : True,
                'data' : {
                    'order_id' : order.order_id,
                    'order_booking_id' : order.order_booking_id
                }
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class GenOrderCode(APIView):
    def get(self,request):
        try:
            data = request.GET.get
            channel_id = data('channel')
            channel = ChannelType.objects.using(db_blue_tree).get(channel_type_id = channel_id)
            booking_code = generate_booking(channel.channel_code)
            return Response(booking_code,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class GetOrderById(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            order_id = data('order_id')
            order = Order.objects.using(db_blue_tree).get(order_id = order_id)
            channel = ChannelType.objects.using(db_blue_tree).filter(channel_type_id = order.order_channel_id).values()
            order = {
                "order_id": order.order_id,
                "order_channel_id": channel[0],
                "order_booking_id": order.order_booking_id,
                "order_id_order_agent": order.order_id_order_agent,
                "order_agent_name": order.order_agent_name,
                "order_booking_date": order.order_booking_date,
                "order_use_date": order.order_use_date,
                "order_customer_name": order.order_customer_name,
                "order_mobile_phone": order.order_mobile_phone,
                "order_email": order.order_email,
                "order_number_of_people": order.order_number_of_people,
                "order_credit_term": order.order_credit_term,
                "order_status": order.order_status,
                "order_status_policy": order.order_status_policy,
                "order_payment_slip": str(order.order_payment_slip),
                "order_comment": order.order_comment,
                "order_information": order.order_information,
                "order_customer_fill": order.order_customer_fill,
                "create_at": order.create_at,
                "update_at": order.update_at
            }
            res = {
                'msg' : True,
                'data' : order
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)

class GetChannelType(APIView):
    def get(self, request):
        try:
            channel = ChannelType.objects.using(db_blue_tree).filter(channel_status = 1, delete_at = None).values()
            res = {
                'msg' : True,
                'data' : channel
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response({'msg':False},status=status.HTTP_400_BAD_REQUEST)