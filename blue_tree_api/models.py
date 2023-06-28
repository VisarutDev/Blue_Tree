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
    booking_status = models.IntegerField(default=0) #0 = waiting for service, 1 = service has been received
    booking_status_policy = models.BooleanField(default=False) #Policy
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)


    def jsonFormat(self):
        data = {
            'booking_id' : self.booking_id,
            'booking_agent_com' : self.booking_agent_com,
            'booking_customer_first_name' : self.booking_customer_first_name,
            'booking_customer_last_name' : self.booking_customer_last_name,
            'booking_email' : self.booking_email,
            'booking_age' : self.booking_age,
            'booking_gender' : self.booking_gender,
            'booking_tel' : self.booking_tel,
            'booking_voucher_code' : self.booking_voucher_code,
            'booking_booking_id' : self.booking_booking_id,
            'booking_status_policy' : self.booking_status_policy,
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
    type_group_status = models.BooleanField(default=True)
    type_group_file = models.BooleanField(default=False)
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
    info_detail_info = models.ForeignKey(UserBooking, related_name='info_detail_booking_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_detail_status_policy = models.BooleanField(default=False) #Policy
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
    info_list_booking = models.ForeignKey(UserBooking, related_name='info_list_booking_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_list_status_policy = models.BooleanField(default=False) #Policy
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
class InformationDetailFile(models.Model):
    class Meta:
        db_table = 'information_detail_file'
    info_detail_file_id = models.AutoField(primary_key=True)
    info_detail_file = models.FileField(upload_to='file/blue_tree/detail_file/', default='file/none/no_file.pdf')
    info_detail_file_info = models.ForeignKey(InformationDetail,related_name='info_detail_file_info_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_detail_file_booking = models.ForeignKey(UserBooking, related_name='info_detail_file_booking_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    info_detail_file_status_policy = models.BooleanField(default=False) #Policy
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)