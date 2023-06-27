from django.db import models
from django.contrib.postgres.fields import JSONField

# class FillType(models.Model):
#     class Meta:
#         db_table = 'fill_type'
#     fill_type_id = models.AutoField(primary_key=True)
#     fill_type_name = models.CharField(max_length=55,blank=True)
#     fill_type_status = models.IntegerField(default=1) # 0 = inactivate, 1 = activate
#     create_at = models.DateTimeField(auto_now_add=True, blank=True)
#     update_at = models.DateTimeField(auto_now = True, blank = True)
#     delete_at = models.DateTimeField(null=True)

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