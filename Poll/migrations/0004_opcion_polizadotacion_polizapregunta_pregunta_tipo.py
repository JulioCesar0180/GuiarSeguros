# Generated by Django 3.1 on 2020-11-08 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20201013_1250'),
        ('Poll', '0003_auto_20201013_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Tipo de Pregunta',
                'verbose_name_plural': 'Tipos de Preguntas',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.tipo')),
            ],
            options={
                'verbose_name': 'Pregunta',
                'verbose_name_plural': 'Preguntas',
            },
        ),
        migrations.CreateModel(
            name='PolizaPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poliza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.subpoliza')),
                ('pregunta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.pregunta')),
            ],
            options={
                'verbose_name': 'Intermedia Poliza-Pregunta',
                'verbose_name_plural': 'Intermedia Polizas-Preguntas',
            },
        ),
        migrations.CreateModel(
            name='PolizaDotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dotacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Home.dotacion')),
                ('poliza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.subpoliza')),
            ],
            options={
                'verbose_name': 'Intermedia Poliza-Dotacion',
                'verbose_name_plural': 'Intermedia Polizas-Preguntas',
            },
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
                ('riesgo', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pregunta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.pregunta')),
            ],
            options={
                'verbose_name': 'Opcion',
                'verbose_name_plural': 'Opciones',
            },
        ),
    ]
