# Generated by Django 3.2 on 2023-06-28 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blue_tree_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationdetail',
            name='info_detail_status',
        ),
        migrations.RemoveField(
            model_name='informationdetaillist',
            name='info_list_status',
        ),
        migrations.RemoveField(
            model_name='typegroup',
            name='type_group_stauts',
        ),
        migrations.AddField(
            model_name='informationdetail',
            name='info_detail_status_policy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='informationdetaillist',
            name='info_list_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='info_list_booking_id', to='blue_tree_api.userbooking'),
        ),
        migrations.AddField(
            model_name='informationdetaillist',
            name='info_list_status_policy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='typegroup',
            name='type_group_file',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='typegroup',
            name='type_group_status',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='InformationDetailFile',
            fields=[
                ('info_detail_file_id', models.AutoField(primary_key=True, serialize=False)),
                ('info_detail_file', models.FileField(default='file/none/no_file.pdf', upload_to='file/blue_tree/detail_file/')),
                ('info_detail_file_status_policy', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('info_detail_file_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='info_detail_file_booking_id', to='blue_tree_api.userbooking')),
                ('info_detail_file_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='info_detail_file_info_id', to='blue_tree_api.informationdetail')),
            ],
            options={
                'db_table': 'information_detail_file',
            },
        ),
    ]
