# Generated by Django 3.1 on 2021-01-04 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0011_auto_20201212_2109'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PolizaPregunta',
            new_name='PolizaOpcion',
        ),
        migrations.AlterModelOptions(
            name='polizaopcion',
            options={'verbose_name': 'Intermedia Poliza-Opcion', 'verbose_name_plural': 'Intermedia Polizas-Opciones'},
        ),
        migrations.RemoveField(
            model_name='polizaopcion',
            name='pregunta',
        ),
        migrations.AddField(
            model_name='polizaopcion',
            name='opcion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.opcion'),
        ),
    ]
