from django.db import models
from django.contrib.postgres.fields import JSONField

class FillList(models.Model):
    class Meta:
        db_table = 'fill_list'
    fill_id = models.AutoField(primary_key=True)
    fill_name = models.CharField(max_length=55, blank=True, null=True)
    fill_type = models.CharField(max_length=55, blank=True, null=True)
    # fill_type = models.ForeignKey(FillType,related_name='fill_type_id_id', on_delete=models.DO_NOTHING)
    fill_status = models.IntegerField(default=1) #0 = inactivate, 1 = activate, 2 = delete
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True)

class SubFillList(models.Model):
    class Meta:
        db_table = 'sub_fill_list'
    sub_fill_id = models.AutoField(primary_key=True)
    sub_fill_list = models.ForeignKey(FillList, related_name='sub_fill_list_id', on_delete=models.DO_NOTHING)
    sub_fill_name = models.CharField(max_length=55, blank=True, null=True)
    sub_fill_status = models.IntegerField(default=1) #0 = inactivate, 1 = activate, 2 = delete
    sub_fill_description = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True)

class ChannelType(models.Model):
    class Meta:
        db_table = 'chnnel_type'
    channel_type_id = models.AutoField(primary_key=True)
    channel_type_name = models.CharField(max_length=55)
    channel_code = models.CharField(max_length=10)
    channel_status = models.IntegerField(default=1) #0 = inactivate, 1 = activate
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True)

class Order(models.Model):
    class Meta:
        db_table = 'order'
    order_id = models.AutoField(primary_key=True)
    order_channel = models.ForeignKey(ChannelType, related_name='order_channel_id', on_delete=models.DO_NOTHING)
    order_booking_id = models.CharField(max_length=55, blank=True)
    order_id_order_agent = models.CharField(max_length=55, blank=True)
    order_agent_name = models.CharField(max_length=100, blank=True)
    order_booking_date = models.DateField(blank=True)
    order_use_date = models.DateField(blank=True)
    order_customer_name = models.CharField(max_length=100, blank=True)
    order_mobile_phone = models.CharField(max_length=10)
    order_email = models.CharField(max_length=100,blank=True,null=True)
    order_number_of_people = models.IntegerField()
    order_credit_term = models.IntegerField()
    order_status = models.IntegerField(default=0) #0 = waiting for service, 1 = service has been received, 2 = delete
    order_status_policy = models.BooleanField(default=False)
    order_payment_slip = models.ImageField(upload_to='payment/slip/', default='payment/slip/no_slip.png', null=True, blank=True)
    order_comment = models.CharField(max_length=255, blank=True)
    order_information = models.CharField(max_length=255, blank=True)
    order_customer_fill = JSONField()
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True)

class Users(models.Model):
    class Meta:
        db_table = 'users'
    users_id = models.AutoField(primary_key=True)
    users_verify = models.IntegerField(default=0) # 0 = unconfirmed for email, 1 = confirmed for email
    users_status = models.IntegerField(default=0) # 0 = chang password status, 1 = on use, 2 = delete
    users_first_name = models.CharField(max_length=150, null=True)
    users_last_name = models.CharField(max_length=150, null=True)
    users_email = models.CharField(max_length=100, null=True)
    users_password = models.CharField(max_length=200)
    users_tel = models.IntegerField(max_length=12, null=True)
    users_image = models.ImageField(upload_to='img/users/', default='img/none/no_img.png',null=True, blank=True)
    users_rank = models.IntegerField(default=0)
    users_point = models.IntegerField(default=0)
    users_role = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    users_activate_at = models.DateTimeField(null=True, blank=True)
    delete_at = models.DateTimeField(null=True)

class UsersToken(models.Model):
    class Meta:
        db_table = 'users_token'
    users_token_id = models.AutoField(primary_key=True)
    users_token_key = models.CharField(max_length = 255,blank=True)
    users_token_refresh = models.CharField(max_length = 255,blank=True)
    users_token_users = models.ForeignKey(Users, related_name='users_token_users_id', on_delete=models.DO_NOTHING)
    users_token_status = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

class BannerApp(models.Model):
    class Meta:
        db_table = 'banner_app'
    banner_id = models.AutoField(primary_key=True)
    banner_name_th = models.CharField(max_length=255, blank=True, null=True)
    banner_name_en = models.CharField(max_length=255, blank=True, null=True)
    banner_description_th = models.CharField(max_length=255, blank=True, null=True)
    banner_description_en = models.CharField(max_length=255, blank=True, null=True)
    banner_image = models.ImageField(upload_to='img/banner', default='img/none/no_banner.png', null=True, blank=True)
    banner_status = models.IntegerField(default=1)# 0 = close, 1 = open, 2 = delete
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class ServiceApp(models.Model):
    class Meta:
        db_table = 'service_app'
    service_id = models.AutoField(primary_key=True)
    service_name_th = models.CharField(max_length=150, blank=True, null=True)
    service_name_en = models.CharField(max_length=150, blank=True, null=True)
    service_description_th = models.CharField(max_length=150, blank=True, null=True)
    service_description_en = models.CharField(max_length=150, blank=True, null=True)
    service_link = models.CharField(max_length=255, null=True)
    service_status = models.IntegerField(default=1)# 0 = close, 1 = open, 2 = delete
    service_icon = models.ImageField(upload_to='img/service', default='img/none/no_icon.png', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class PromotionApp(models.Model):
    class Meta:
        db_table = 'promotion_app'
    promotion_id = models.AutoField(primary_key=True)
    promotion_code = models.CharField(max_length=50, blank=True, null=True)
    promotion_name_th = models.CharField(max_length=255, blank=True, null=True)
    promotion_name_en = models.CharField(max_length=255, blank=True, null=True)
    promotion_description_th = models.CharField(max_length=255, blank=True, null=True)
    promotion_description_en = models.CharField(max_length=255, blank=True, null=True)
    promotion_discount_price = models.FloatField(default=0)
    promotion_maximum_discount = models.IntegerField(default=0)
    promotion_status = models.IntegerField(default=1)# 0 = close, 1 = open, 2 = delete
    promotion_image = models.ImageField(upload_to='img/promotion', default='img/none/no_img.png', null=True, blank=True)
    promotion_date_start = models.DateTimeField(null=True, blank=True)
    promotion_date_end = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class HappeningApp(models.Model):
    class Meta:
        db_table = 'happening_app'
    happening_id = models.AutoField(primary_key=True)
    happening_name_th = models.CharField(max_length=255, blank=True, null=True)
    happening_name_en = models.CharField(max_length=255, blank=True, null=True)
    happening_description_th = models.CharField(max_length=255, blank=True, null=True)
    happening_description_en = models.CharField(max_length=255, blank=True, null=True)
    happening_discount_price = models.FloatField(default=0)
    happening_status = models.IntegerField(default=1)# 0 = close, 1 = open, 2 = delete
    happening_product = models.IntegerField(null=True)
    happening_image = models.ImageField(upload_to='img/happening', default='img/none/no_img.png', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

class NotificationApp(models.Model):
    class Meta:
        db_table = 'notification_app'
    notification_id = models.AutoField(primary_key=True)
    notification_name_th = models.CharField(max_length=255, blank=True, null=True)
    notification_name_en = models.CharField(max_length=255, blank=True, null=True)
    notification_description_th = models.CharField(max_length=255, blank=True, null=True)
    notification_description_en = models.CharField(max_length=255, blank=True, null=True)
    notification_status = models.IntegerField(default=1)# 0 = close, 1 = open on use, 2 = delete
    notification_image = models.ImageField(upload_to='img/notification', default='img/none/no_img.png', null=True, blank=True)
    notification_date_start = models.DateTimeField(null=True, blank=True)
    notification_date_end = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)