from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.
from Poll.models import *


class Town(models.Model):
    name_town_t = models.CharField(max_length=50)

    def __str__(self):
        return self.name_town_t


class City(models.Model):
    name_city = models.CharField(max_length=50)
    name_town = models.ForeignKey(Town, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_city


class UserGuiarManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, rut, password, **extra_fields):
        if not rut:
            raise ValueError('Error')
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, rut, password, **extra_fields):
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self.db)
        return user


class UserGuiar(AbstractUser):
    rut = models.CharField(max_length=12, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    town = models.CharField(max_length=50)
    address = models.CharField(max_length=100, default="")
    seniority = models.PositiveSmallIntegerField(default=0)

    # Datos del representante
    manager = models.OneToOneField('BusinessManager', on_delete=models.CASCADE, null=True, blank=True)

    # Ventas Anuales
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True)

    # Dotacion Empresa
    n_emp_hired = models.PositiveIntegerField(null=True, default=0)
    n_cont_emp = models.PositiveIntegerField(null=True, default=0)
    n_veh_com_light = models.PositiveIntegerField(null=True, default=0)
    n_veh_com_cont = models.PositiveIntegerField(null=True, default=0)
    n_veh_com_heavy = models.PositiveIntegerField(null=True, default=0)
    n_veh_com_heavy_cont = models.PositiveIntegerField(null=True, default=0)
    n_mach_heavy = models.PositiveIntegerField(null=True, default=0)
    n_mach_heavy_cont = models.PositiveIntegerField(null=True, default=0)

    # Procesos de la Empresa
    process = models.ManyToManyField(ProcessBusiness)

    # Transporte
    transport = models.ManyToManyField(TransportProcess, blank=True)

    # Manufactura
    manufacture = models.ManyToManyField(ManufactureProcess, blank=True)

    # Construccion
    building = models.ManyToManyField(BuildingProcess, blank=True)

    # Servicios Generales
    general_services = models.ManyToManyField(GeneralServicesProcess, blank=True)

    # Elementos de manejo de riesgos
    risk_management = models.ForeignKey(RiskManagement, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Prevencionista de Riesgo
    risk_prevent = models.ForeignKey(RiskPreventionPersonal, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Explosives Control
    explosive_control = models.ManyToManyField(ExplosiveControl)
    # Electricity Control
    electricity_control = models.ManyToManyField(ElectricityControl)
    # Substance Control
    substance_control = models.ManyToManyField(SubstanceControl)
    # Height Control
    height_control = models.ManyToManyField(HeightControl)

    is_admin = models.BooleanField(default=False)
    objects = UserGuiarManager()
    USERNAME_FIELD = 'rut'
    EMAIL_FIELD = 'manager'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class BusinessManager(models.Model):
    rut_bm = models.CharField(max_length=12, primary_key=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveIntegerField()

    def __str__(self):
        return self.rut_bm
