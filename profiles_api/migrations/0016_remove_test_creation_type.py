# Generated by Django 2.2 on 2020-08-15 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0015_auto_20200815_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='creation_type',
        ),
    ]
