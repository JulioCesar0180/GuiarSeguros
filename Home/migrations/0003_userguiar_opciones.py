# Generated by Django 3.1 on 2020-11-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0006_auto_20201108_1858'),
        ('Home', '0002_auto_20201013_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='userguiar',
            name='opciones',
            field=models.ManyToManyField(blank=True, to='Poll.Opcion'),
        ),
    ]
