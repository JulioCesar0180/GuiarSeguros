# Generated by Django 3.1.1 on 2020-09-18 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20200917_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='name_town',
        ),
    ]