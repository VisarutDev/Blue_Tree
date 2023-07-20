from datetime import datetime
from venv import create
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from blue_tree.settings import db_blue_tree
from .utils import generate_booking, UploadImage
from blue_tree_app.utils import Hash
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
                orders = orders.filter(Q(order_booking_id__icontains = search) | Q(order_customer_name__icontains = search))

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
            res = {
                'msg' : True,
                'data' : {
                    'booking_code' : booking_code,
                    'channel' : {
                        'channel_type_id' : channel.channel_type_id,
                        'channel_type_name' : channel.channel_type_name,
                        'channel_code' : channel.channel_code
                    }
                }
            }
            return Response(res,status=status.HTTP_200_OK)
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
class ManagePromotion(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            promotion_id = data('promotion_id')
            get_promotion = PromotionApp.objects.using(db_blue_tree).filter(promotion_id = promotion_id, delete_at = None).values()
            get_promotion[0]['promotion_image'] = str(get_promotion[0]['promotion_image'])
            res = {
                'msg' : True,
                'data' : get_promotion[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            get_promotion = PromotionApp.objects.using(db_blue_tree).filter(promotion_id = data['promotion_id'])
            if data['promotion_image']:
                promotion_img = data['promotion_image']
                get_image = PromotionApp.objects.using(db_blue_tree).get(promotion_id = data['promotion_id'])
                name = str("promotion") + str(data['promotion_id']) + "_" + str(date_time)
                promotion_img = UploadImage(promotion_img,name)
                get_image.promotion_image = promotion_img
                get_image.save()

            data_promotion = {
                'promotion_code' : data['promotion_code'],
                'promotion_name_th' : data['promotion_name_th'],
                'promotion_name_en' : data['promotion_name_en'],
                'promotion_description_th' : data['promotion_description_th'],
                'promotion_description_en' : data['promotion_description_en'],
                'promotion_discount_price' : data['promotion_discount_price'],
                'promotion_status' : data['promotion_status'],
                'promotion_date_start' : data['promotion_date_start'],
                'promotion_date_end' : data['promotion_date_end'],
                'promotion_maximum_discount' : data['promotion_maximum_discount'],
                'update_at' : date_time
            }
            get_promotion.update(**data_promotion)
            get_promotion = get_promotion.values()
            get_promotion[0]['promotion_image'] = str(get_promotion[0]['promotion_image'])
            res = {
                'msg' : True,
                'data' : get_promotion[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            if data['promotion_image']:
                promotion_img = data['promotion_image']
                name = str("promotion") + "_" + str(date_time)
                promotion_img = UploadImage(promotion_img,name)
            else:
                promotion_img = None

            data_promotion = {
                'promotion_code' : data['promotion_code'],
                'promotion_name_th' : data['promotion_name_th'] if 'promotion_name_th' in data else None,
                'promotion_name_en' : data['promotion_name_en'] if 'promotion_name_en' in data else None,
                'promotion_description_th' : data['promotion_description_th'] if 'promotion_description_th' in data else None,
                'promotion_description_en' : data['promotion_description_en'] if 'promotion_description_en' in data else None,
                'promotion_discount_price' : data['promotion_discount_price'] if 'promotion_discount_price' in data else None,
                'promotion_status' : data['promotion_status'] if 'promotion_status' in data else 1,
                'promotion_date_start' : data['promotion_date_start'] if 'promotion_date_start' in data else None,
                'promotion_date_end' : data['promotion_date_end'] if 'promotion_date_end' in data else None,
                'promotion_maximum_discount' : data['promotion_maximum_discount'] if 'promotion_maximum_discount' in data else None,
                'promotion_image' : promotion_img
            }
            promotion = PromotionApp.objects.using(db_blue_tree).create(**data_promotion)
            data_promotion['promotion_id'] = promotion.promotion_id
            data_promotion['promotion_image'] = str(data_promotion['promotion_image'])
            res = {
                'msg' : True,
                'data' : data_promotion
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.GET.get
            date_time = datetime.now()
            promotion = PromotionApp.objects.using(db_blue_tree).get(promotion_id = data('promotion_id'))
            promotion.delete_at = date_time
            promotion.promotion_status = 2
            promotion.save()
            res = {
                'msg' : True,
                'data' : "delete success promotion id " + str(data('promotion_id'))
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class ChangStatusPromotion(APIView):
    def put(self, request):
        try:
            data = request.data
            promotion = PromotionApp.objects.using(db_blue_tree).get(promotion_id = data['promotion_id'], delete_at = None)
            promotion.promotion_status = data['promotion_status']
            promotion.save()
            res = {
                'msg' : True,
                'data' : "change status success promotion id " + str(data['promotion_id']) + " status " + str(data['promotion_status'])
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class GetAllPromotion(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            page_size = int(data("page_size"))
            current_page = int(data("current_page"))
            promotions = PromotionApp.objects.using(db_blue_tree).filter(~Q(promotion_status = 2),delete_at = None)
            for promotion in promotions:
                promotion.promotion_image = str(promotion.promotion_image)
            promotions = promotions.values()
            res = {
                'msg' : True,
                'data' : promotions[page_size * (current_page - 1): page_size * current_page]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class ManageHappening(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            happening_id = data('happening_id')
            get_happening = HappeningApp.objects.using(db_blue_tree).filter(happening_id = happening_id, delete_at = None).values()
            get_happening[0]['happening_image'] = str(get_happening[0]['happening_image'])
            res = {
                'msg' : True,
                'data' : get_happening[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            get_happening = HappeningApp.objects.using(db_blue_tree).filter(happening_id = data['happening_id'])
            if data['happening_image']:
                get_image = HappeningApp.objects.using(db_blue_tree).get(happening_id = data['happening_id'])
                happening_img = data['happening_image']
                name = str("happening") + "_" + str(date_time)
                happening_img = UploadImage(happening_img,name)
                get_image.happening_image = happening_img
                get_image.save()

            data_happening = {
                'happening_name_th' : data['happening_name_th'],
                'happening_name_en' : data['happening_name_en'],
                'happening_description_th' : data['happening_description_th'],
                'happening_description_en' : data['happening_description_en'],
                'happening_discount_price' : data['happening_discount_price'],
                'happening_status' : data['happening_status'],
                'happening_product' : data['happening_product'],
                'update_at' : date_time
            }
            get_happening.update(**data_happening)
            get_happening = get_happening.values()
            get_happening[0]['happening_image'] = str(get_happening[0]['happening_image'])
            res = {
                'msg' : True,
                'data' : get_happening[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            if data['happening_image']:
                happening_img = data['happening_image']
                name = str("happening") + "_" + str(date_time)
                happening_img = UploadImage(happening_img,name)
            else:
                happening_img = None

            data_happening = {
                'happening_name_th' : data['happening_name_th'] if 'happening_name_th' in data else None,
                'happening_name_en' : data['happening_name_en'] if 'happening_name_en' in data else None,
                'happening_description_th' : data['happening_description_th'] if 'happening_description_th' in data else None,
                'happening_description_en' : data['happening_description_en'] if 'happening_description_en' in data else None,
                'happening_discount_price' : data['happening_discount_price'] if 'happening_discount_price' in data else None,
                'happening_status' : data['happening_status'] if 'happening_status' in data else 1,
                'happening_product' : data['happening_product'] if 'happening_product' in data else None,
                'happening_image' : happening_img
            }
            happening = HappeningApp.objects.using(db_blue_tree).create(**data_happening)
            data_happening['happening_id'] = happening.happening_id
            data_happening['happening_image'] = str(data_happening['happening_image'])
            res = {
                'msg' : True,
                'data' : data_happening
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.GET.get
            date_time = datetime.now()
            happening = HappeningApp.objects.using(db_blue_tree).get(happening_id = data('happening_id'))
            happening.delete_at = date_time
            happening.happening_status = 2
            happening.save()
            res = {
                'msg' : True,
                'data' : "delete success happening id " + str(data('happening_id'))
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class ChangStatusHappening(APIView):
    def put(self, request):
        try:
            data = request.data
            happening = HappeningApp.objects.using(db_blue_tree).get(happening_id = data['happening_id'], delete_at = None)
            happening.happening_status = data['happening_status']
            happening.save()
            res = {
                'msg' : True,
                'data' : "change status success happening id " + str(data['happening_id']) + " status " + str(data['happening_status'])
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class GetAllHappening(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            page_size = int(data("page_size"))
            current_page = int(data("current_page"))
            happenings = HappeningApp.objects.using(db_blue_tree).filter(~Q(happening_status = 2),delete_at = None)
            for happening in happenings:
                happening.happening_image = str(happening.happening_image)
            happenings = happenings.values()
            res = {
                'msg' : True,
                'data' : happenings[page_size * (current_page - 1): page_size * current_page]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class ManageBanner(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            banner_id = data('banner_id')
            get_banner = BannerApp.objects.using(db_blue_tree).filter(banner_id = banner_id, delete_at = None).values()
            get_banner[0]['banner_image'] = str(get_banner[0]['banner_image'])
            res = {
                'msg' : True,
                'data' : get_banner[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            get_banner = BannerApp.objects.using(db_blue_tree).filter(banner_id = data['banner_id'])
            if data['banner_image']:
                get_image = BannerApp.objects.using(db_blue_tree).get(banner_id = data['banner_id'])
                banner_img = data['banner_image']
                name = str("banner") + "_" + str(date_time)
                banner_img = UploadImage(banner_img,name)
                get_image.banner_image = banner_img
                get_image.save()

            data_banner = {
                'banner_name_th' : data['banner_name_th'],
                'banner_name_en' : data['banner_name_en'],
                'banner_description_th' : data['banner_description_th'],
                'banner_description_en' : data['banner_description_en'],
                'banner_status' : data['banner_status'],
                'update_at' : date_time
            }
            get_banner.update(**data_banner)
            get_banner = get_banner.values()
            get_banner[0]['banner_image'] = str(get_banner[0]['banner_image'])
            res = {
                'msg' : True,
                'data' : get_banner[0]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            if data['banner_image']:
                banner_img = data['banner_image']
                name = str("banner") + "_" + str(date_time)
                banner_img = UploadImage(banner_img,name)
            else:
                banner_img = None

            data_banner = {
                'banner_name_th' : data['banner_name_th'] if 'banner_name_th' in data else None,
                'banner_name_en' : data['banner_name_en'] if 'banner_name_en' in data else None,
                'banner_description_th' : data['banner_description_th'] if 'banner_description_th' in data else None,
                'banner_description_en' : data['banner_description_en'] if 'banner_description_en' in data else None,
                'banner_status' : data['banner_status'] if 'banner_status' in data else 1,
                'banner_image' : banner_img
            }
            banner = BannerApp.objects.using(db_blue_tree).create(**data_banner)
            data_banner['banner_id'] = banner.banner_id
            data_banner['banner_image'] = str(data_banner['banner_image'])
            res = {
                'msg' : True,
                'data' : data_banner
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.GET.get
            date_time = datetime.now()
            banner = BannerApp.objects.using(db_blue_tree).get(banner_id = data('banner_id'))
            banner.delete_at = date_time
            banner.banner_status = 2
            banner.save()
            res = {
                'msg' : True,
                'data' : "delete success banner id " + (data('banner_id'))
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class ChangStatusBanner(APIView):
    def put(self, request):
        try:
            data = request.data
            banner = BannerApp.objects.using(db_blue_tree).get(banner_id = data['banner_id'], delete_at = None)
            banner.banner_status = data['banner_status']
            banner.save()
            res = {
                'msg' : True,
                'data' : "change status success banner id " + str(data['banner_id']) + " status " + str(data['banner_status'])
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            raise
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class GetAllBanner(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            page_size = int(data("page_size"))
            current_page = int(data("current_page"))
            banners = BannerApp.objects.using(db_blue_tree).filter(~Q(banner_status = 2),delete_at = None)
            for banner in banners:
                banner.banner_image = str(banner.banner_image)
            banners = banners.values()
            res = {
                'msg' : True,
                'data' : banners[page_size * (current_page - 1): page_size * current_page]
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
class ManageUsers(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            users_id = data('users_id')
            get_users = Users.objects.using(db_blue_tree).filter(users_id = users_id, delete_at = None)
            get_users[0].users_image = str(get_users[0].users_image)
            get_users = get_users.values()
            res = {
                'msg' : True,
                'data' : get_users[0]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        try:
            data = request.data
            date_time = datetime.now()
            get_users = Users.objects.using(db_blue_tree).filter(users_id = data['users_id'])

            if data['users_image']:
                get_image = Users.objects.using(db_blue_tree).get(users_id = data['users_id'])
                users_img = data['users_image']
                name = str("users") + "_" + str(date_time)
                users_img = UploadImage(users_img,name)
                get_image.users_image = users_img
                get_image.save()

            users_password = Hash.hash_password(data['users_password'])

            data_users = {
                'users_status':data['users_status'],
                'users_first_name' : data['users_first_name'],
                'users_last_name' : data['users_last_name'],
                'users_email' : data['users_email'],
                'users_password' : users_password,
                'users_tel' : data['users_tel'],
                'users_role':data['users_role'],
                'update_at' : date_time
            }
            get_users.update(**data_users)
            get_users = get_users.values()
            res = {
                'msg' : True,
                'data' : get_users[0]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            data = request.data
            date_time = datetime.now()

            if data['users_image']:
                users_img = data['users_image']
                name = str("users") + "_" + str(date_time)
                users_img = UploadImage(users_img,name)

            users_password = Hash.hash_password(data['users_password'])

            data_users = {
                'users_status':data['users_status'],
                'users_first_name' : data['users_first_name'],
                'users_last_name' : data['users_last_name'],
                'users_email' : data['users_email'],
                'users_password' : users_password,
                'users_tel' : data['users_tel'],
                'users_role':data['users_role'],
                'users_image' : users_img
            }
            users = Users.objects.using(db_blue_tree).create(**data_users)
            data_users['users_image'] = str(data_users['users_image'])
            data_users['users_id'] = users.users_id
            res = {
                'msg' : True,
                'data' : data_users
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        try:
            data = request.GET.get
            date_time = datetime.now()
            get_users = Users.objects.using(db_blue_tree).get(users_id = data('users_id'))
            get_users.users_status = 2
            get_users.delete_at = date_time
            get_users.save()
            res = {
                'msg' : True,
                'data' : "Delete success users id " + str(data('users_id'))
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)
class GetAllUser(APIView):
    def get(self, request):
        try:
            data = request.GET.get
            page_size = int(data('page_size'))
            current_page = int(data('current_page'))
            get_users = Users.objects.using(db_blue_tree).filter(users_status__in = [0,1], delete_at = None)
            for user in get_users:
                user.users_image = str(user.users_image)
            get_users = get_users.values()
            res = {
                'msg' : True,
                'data' : get_users[page_size * (current_page - 1) : page_size * current_page]
            }
            return Response(res,status=status.HTTP_200_OK)
        except:
            return Response(False,status=status.HTTP_400_BAD_REQUEST)