# Generated by Django 3.1 on 2021-05-05 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0016_opcion_cobertura'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poliza',
            options={'verbose_name': 'Ramo', 'verbose_name_plural': 'Ramos'},
        ),
        migrations.AlterModelOptions(
            name='polizaopcion',
            options={'verbose_name': 'Vinculación', 'verbose_name_plural': 'Vinculaciones'},
        ),
        migrations.AlterModelOptions(
            name='subpoliza',
            options={'verbose_name': 'Poliza', 'verbose_name_plural': 'Polizas'},
        ),
        migrations.RemoveField(
            model_name='poliza',
            name='order',
        ),
        migrations.RemoveField(
            model_name='subpoliza',
            name='order',
        ),
    ]