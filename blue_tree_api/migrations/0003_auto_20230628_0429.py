# Generated by Django 3.2 on 2023-06-28 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_tree_api', '0002_auto_20230628_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbooking',
            name='booking_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userbooking',
            name='booking_status_policy',
            field=models.BooleanField(default=False),
        ),
    ]
