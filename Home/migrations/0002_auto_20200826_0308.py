# Generated by Django 3.1 on 2020-08-26 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userguiar',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Home.city'),
        ),
    ]