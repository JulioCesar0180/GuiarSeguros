# Generated by Django 3.1 on 2020-10-13 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0002_auto_20201013_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpoliza',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza'),
        ),
    ]
