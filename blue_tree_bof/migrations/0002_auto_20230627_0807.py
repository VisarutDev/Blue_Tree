# Generated by Django 2.2 on 2023-06-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_tree_bof', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='order_information',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
