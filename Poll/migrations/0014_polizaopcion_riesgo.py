# Generated by Django 3.1 on 2021-01-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0013_polizadependencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='polizaopcion',
            name='riesgo',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]