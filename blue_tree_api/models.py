from django.db import models

class UserBooking(models.Model):
    class Meta:
        db_table = 'user_booking'
    booking_id = models.AutoField(primary_key=True)
    booking_agent_com = models.CharField(max_length=55, blank=True, null=True)
    booking_customer_first_name = models.CharField(max_length=55, blank=True, null=True)
    booking_customer_last_name = models.CharField(max_length=55, blank=True, null=True)
    booking_email = models.EmailField(max_length=55, blank=True, null=True)
    booking_age = models.IntegerField(default=0)
    booking_gender = models.CharField(max_length=10, blank=True, null=True)
    booking_tel = models.IntegerField(default=0)
    booking_voucher_code = models.CharField(max_length=55, blank=True, null=True, default=None)
    booking_booking_id = models.CharField(max_length=55, blank=True, null=True, default=None)
    # booking_status = models.BooleanField(default=0)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.info_id)

    def jsonFormat(self):
        data = {
            'booking_id' : self.booking_id,
            'booking_agent_com' : self.booking_agent_com,
            'booking_customer_first_name' : self.booking_customer_first_name,
            'booking_customer_last_name' : self.booking_customer_last_name,
            'booking_email' : self.booking_email,
            'booking_voucher_code' : self.booking_voucher_code,
            'booking_booking_id' : self.booking_booking_id,
            # 'booking_status' : self.booking_status,
            'create_at' : self.create_at,
            'update_at' : self.update_at
        }
        return data
class TypeGroup(models.Model):
    class Meta:
        db_table = 'type_group'
    type_group_id = models.AutoField(primary_key=True)
    type_group_people = models.IntegerField(default=0)
    type_group_detail = models.CharField(max_length=20)
    type_group_stauts = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
class InformationDetail(models.Model):
    class Meta:
        db_table = 'information_detail'
    info_detail_id = models.AutoField(primary_key=True)
    info_detail_country = models.CharField(max_length=100, blank=True, null=True)
    info_detail_live_phuket = models.BooleanField(default=False)
    info_detail_people = models.IntegerField(default=0)
    info_detail_type = models.ForeignKey(TypeGroup, related_name='info_detail_type_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    # info_detail_first_name = models.CharField(max_length=255, blank=True, null=True)
    # info_detail_last_name = models.CharField(max_length=255, blank=True, null=True)
    # info_detail_age = models.IntegerField(default=0)
    # info_detail_gender = models.CharField(max_length=10, blank=True, null=True)
    # info_detail_email = models.EmailField(max_length=55, blank=True, null=True)
    # info_detail_tel = models.IntegerField(default=0)
    info_detail_info = models.ForeignKey(UserBooking, related_name='info_detail_booking_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_detail_status = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
class InformationDetailList(models.Model):
    class Meta:
        db_table = 'information_detail_list'
    info_list_id = models.AutoField(primary_key=True)
    info_list_first_name = models.CharField(max_length=255, blank=True, null=True)
    info_list_last_name = models.CharField(max_length=255, blank=True, null=True)
    info_list_age = models.IntegerField(default=0)
    info_list_gender = models.CharField(max_length=10, blank=True, null=True)
    info_list_info = models.ForeignKey(InformationDetail,related_name='info_list_info_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_list_status = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)