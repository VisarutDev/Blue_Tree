# Generated by Django 3.2 on 2023-06-29 04:02

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blue_tree_api', '0004_typegroup_type_group_people_max'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationdetail',
            name='info_detail_people',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='informationdetail',
            name='info_detail_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='typegroup',
            name='type_group_detail',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
