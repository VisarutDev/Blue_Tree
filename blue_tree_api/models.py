from django.db import models

class UserRole(models.Model):
    class Meta:
        db_table = 'user_role'

    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=55, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.role_id)

class Users(models.Model):
    class Meta:
        db_table = 'users'
    users_id = models.AutoField(primary_key=True)
    users_role = models.ForeignKey(UserRole, related_name='users_users_role', on_delete=models.DO_NOTHING)
    users_verify = models.BooleanField(default=False)
    users_country_tel = models.CharField(max_length=55, blank=True, null=True)
    users_address = models.CharField(max_length=255, blank=True, null=True)
    users_tel = models.CharField(max_length=9, unique=True)
    users_email = models.EmailField(max_length=55, blank=True, null=True)
    users_password = models.CharField(max_length=255, blank=True)
    users_facebook_id = models.CharField(max_length=55, unique=True, blank=True, null=True)
    users_first_name = models.CharField(max_length=55, blank=True)
    users_last_name = models.CharField(max_length=55, blank=True)
    # users_image = models.ImageField(upload_to='img/users/', default='img/none/no_img.png', null=True, blank=True)
    users_pdpa_status = models.IntegerField(default=0, blank=True, null=True)
    users_onDelete = models.DateTimeField(null=True)
    users_original_tel = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
