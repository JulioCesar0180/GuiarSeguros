# Generated by Django 3.1.1 on 2020-09-18 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_electricity', models.CharField(max_length=10)),
                ('value_ri_electricity', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Confirmación de Riesgo Electricos',
                'verbose_name_plural': 'Confirmación Riesgos Electricos',
            },
        ),
        migrations.CreateModel(
            name='ExplosiveConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_explosive', models.CharField(max_length=10)),
                ('value_ri_explosive', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Confirmación de Riesgo Explosivo',
                'verbose_name_plural': 'Confirmación de Riesgos Explosivos',
            },
        ),
        migrations.CreateModel(
            name='HeightConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_height', models.CharField(max_length=10)),
                ('value_ri_height', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Confirmación de Riesgo en Altura',
                'verbose_name_plural': 'Confirmación de Riesgos en Altura',
            },
        ),
        migrations.CreateModel(
            name='Poliza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Poliza',
                'verbose_name_plural': 'Polizas',
            },
        ),
        migrations.CreateModel(
            name='ProcessBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Proceso Empresarial',
                'verbose_name_plural': 'Procesos Empresariales',
            },
        ),
        migrations.CreateModel(
            name='RiskManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_risk', models.CharField(max_length=100)),
                ('ri_risk', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Manejo de Riesgo',
                'verbose_name_plural': 'Manejo de Riesgos',
            },
        ),
        migrations.CreateModel(
            name='RiskPreventionPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_prevent', models.CharField(max_length=100)),
                ('ri_prevent', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Prevesión de Riesgo',
                'verbose_name_plural': 'Prevension de Riesgos',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='SubstanceConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_substance', models.CharField(max_length=10)),
                ('value_ri_substance', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Confirmación de Riesgo de Sustancia Peligrosa',
                'verbose_name_plural': 'Confirmación de Riesgos de Sustancias Peligrosas',
            },
        ),
        migrations.CreateModel(
            name='TransportProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_transport', models.CharField(max_length=100)),
                ('ri_transport', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Proceso de Transporte',
                'verbose_name_plural': 'Procesos de Transportes',
            },
        ),
        migrations.CreateModel(
            name='SubstanceControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('substance_control', models.CharField(max_length=255)),
                ('ri_substance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Manejo de Sustancia Peligrosa',
                'verbose_name_plural': 'Manejo de Sustancias Peligrosas',
            },
        ),
        migrations.CreateModel(
            name='ManufactureProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_manufacture', models.CharField(max_length=100)),
                ('ri_manufacture', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Proceso de Manufactura',
                'verbose_name_plural': 'Procesos de Manufacturas',
            },
        ),
        migrations.CreateModel(
            name='HeightControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height_control', models.CharField(max_length=255)),
                ('ri_height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Manejo de Riesgo en Altura',
                'verbose_name_plural': 'Manejo de Riesgos en Altura',
            },
        ),
        migrations.CreateModel(
            name='GeneralServicesProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_service', models.CharField(max_length=100)),
                ('ri_service', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Proceso de Servicio General',
                'verbose_name_plural': 'Procesos de Servicios Generales',
            },
        ),
        migrations.CreateModel(
            name='ExplosiveControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explosive_control', models.CharField(max_length=255)),
                ('ri_explosive', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Manejo de Explosivo',
                'verbose_name_plural': 'Manejo de Explosivos',
            },
        ),
        migrations.CreateModel(
            name='ElectricityControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electricity_control', models.CharField(max_length=255)),
                ('ri_electricity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Manejo de riesgo eléctrico',
                'verbose_name_plural': 'Manejo de riesgos eléctricos',
            },
        ),
        migrations.CreateModel(
            name='DotacionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('min_value', models.PositiveIntegerField()),
                ('max_value', models.PositiveIntegerField()),
                ('ri_value', models.PositiveIntegerField(default=1)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Dotacion Empresa',
                'verbose_name_plural': 'Dotaciones Empresariales',
            },
        ),
        migrations.CreateModel(
            name='BuildingProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_building', models.CharField(max_length=100)),
                ('ri_building', models.DecimalField(decimal_places=2, max_digits=5)),
                ('poliza', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.poliza')),
            ],
            options={
                'verbose_name': 'Proceso de Contrucción',
                'verbose_name_plural': 'Procesos de Construccion',
            },
        ),
    ]
