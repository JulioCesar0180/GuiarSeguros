# Generated by Django 3.1 on 2020-11-21 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0006_auto_20201108_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('riesgo', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('tipo', models.CharField(choices=[(1, 'Procesos'), (2, 'Actividades')], max_length=20)),
            ],
            options={
                'verbose_name': 'Dependencia',
                'verbose_name_plural': 'Dependencias',
            },
        ),
        migrations.AddField(
            model_name='opcion',
            name='dependencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.dependencia'),
        ),
    ]
