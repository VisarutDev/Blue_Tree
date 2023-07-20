from django.utils.crypto import get_random_string
from blue_tree_bof.models import Order
from blue_tree_api.models import UserBooking
from blue_tree.settings import db_blue_tree
import io
import base64
from PIL import Image
from django.core.files.base import ContentFile
import string

def generate_booking(channel_type):
    length = 6
    allowed_chars = string.digits
    unique_code = get_random_string(length=length, allowed_chars=allowed_chars)
    order_code = channel_type + unique_code
    order = UserBooking.objects.using(db_blue_tree).filter(booking_booking_id = order_code)
    if len(order) != 0:
        generate_booking(channel_type)
    return order_code

def UploadImage(image,name):
    image_64_encode = image
    format, imgstr = image_64_encode.split(';base64,')
    image_ascii = imgstr.encode("ascii")
    decoded = base64.decodebytes(image_ascii)
    raw_img_io = io.BytesIO(decoded)
    imgstr = Image.open(raw_img_io)
    # imgstr = imgstr.resize((480, 320))
    img_io = io.BytesIO()
    imgstr.save(img_io, format.split("/")[1], quality=80)

    url_image = ContentFile(img_io.getvalue(),name= name + "." + str(format.split("/")[1]))

    return url_image