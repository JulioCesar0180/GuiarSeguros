# Generated by Django 3.1 on 2020-08-29 19:08

import Home.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessManager',
            fields=[
                ('rut_bm', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_town_t', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserGuiar',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=50)),
                ('address', models.CharField(default='', max_length=100)),
                ('seniority', models.PositiveSmallIntegerField(default=0)),
                ('n_emp_hired', models.PositiveIntegerField(default=0, null=True)),
                ('n_cont_emp', models.PositiveIntegerField(default=0, null=True)),
                ('n_veh_com_light', models.PositiveIntegerField(default=0, null=True)),
                ('n_veh_com_cont', models.PositiveIntegerField(default=0, null=True)),
                ('n_veh_com_heavy', models.PositiveIntegerField(default=0, null=True)),
                ('n_veh_com_heavy_cont', models.PositiveIntegerField(default=0, null=True)),
                ('n_mach_heavy', models.PositiveIntegerField(default=0, null=True)),
                ('n_mach_heavy_cont', models.PositiveIntegerField(default=0, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('building', models.ManyToManyField(blank=True, to='Poll.BuildingProcess')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Home.city')),
                ('electricity_control', models.ManyToManyField(to='Poll.ElectricityControl')),
                ('explosive_control', models.ManyToManyField(to='Poll.ExplosiveControl')),
                ('general_services', models.ManyToManyField(blank=True, to='Poll.GeneralServicesProcess')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('height_control', models.ManyToManyField(to='Poll.HeightControl')),
                ('manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.businessmanager')),
                ('manufacture', models.ManyToManyField(blank=True, to='Poll.ManufactureProcess')),
                ('process', models.ManyToManyField(to='Poll.ProcessBusiness')),
                ('risk_management', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.riskmanagement')),
                ('risk_prevent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Poll.riskpreventionpersonal')),
                ('sales', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Poll.sales')),
                ('substance_control', models.ManyToManyField(to='Poll.SubstanceControl')),
                ('transport', models.ManyToManyField(blank=True, to='Poll.TransportProcess')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', Home.models.UserGuiarManager()),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='name_town',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.town'),
        ),
    ]
