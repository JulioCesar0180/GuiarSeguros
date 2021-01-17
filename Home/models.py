from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.
from Poll.models import Sales, SubPoliza, Opcion


class Town(models.Model):
    name_town_t = models.CharField(max_length=50)

    def __str__(self):
        return self.name_town_t

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"


class City(models.Model):
    name_city = models.CharField(max_length=50)

    def __str__(self):
        return self.name_city

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"


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


class UserGuiar(AbstractBaseUser, PermissionsMixin):
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    town = models.ForeignKey(Town, on_delete=models.DO_NOTHING, null=True)
    address = models.CharField(max_length=100, null=True)
    seniority = models.PositiveSmallIntegerField(null=True, blank=True)

    # Datos del representante
    manager = models.OneToOneField('BusinessManager', on_delete=models.CASCADE, null=True, blank=True)

    # Ventas Anuales
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True)

    is_admin = models.BooleanField(default=False)

    enable_poll = models.BooleanField(default=True)
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

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class BusinessManager(models.Model):
    rut_bm = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.PositiveIntegerField()

    def __str__(self):
        return self.rut_bm

    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"


class RecoveryTokens(models.Model):
    token = models.CharField(max_length=500, default="")
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Token Generado"
        verbose_name_plural = "Tokens Generados"


class DotacionEmpresarial(models.Model):
    cantidad = models.IntegerField(default=0)
    user = models.ForeignKey('UserGuiar', models.DO_NOTHING)
    dotacion = models.ForeignKey('Dotacion', models.DO_NOTHING)

    def __str__(self):
        return self.user.rut + " " + self.dotacion.title

    class Meta:
        verbose_name = "Dotacion Empresa"
        verbose_name_plural = "Dotaciones Empresariales"


class Dotacion(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Dotacion"
        verbose_name_plural = "Dotaciones"


class RangosDotacion(models.Model):
    dotacion = models.ForeignKey('Dotacion', models.DO_NOTHING)
    min_value = models.PositiveIntegerField()
    max_value = models.PositiveIntegerField()
    ri_value = models.PositiveIntegerField(default=1)
    poliza = models.ForeignKey(SubPoliza, models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        if self.max_value > self.min_value:
            return self.dotacion.title + " (" + str(self.min_value) + "-" + str(self.max_value) + ") risk " +\
               str(self.ri_value)
        else:
            return self.dotacion.title + " (" + str(self.min_value) + "+) risk " + str(self.ri_value)

    class Meta:
        verbose_name = "Rango Dotacion"
        verbose_name_plural = "Rangos Dotaciones"


class IntermediaUserOpcion(models.Model):
    user = models.ForeignKey('UserGuiar', models.DO_NOTHING)
    opcion = models.ForeignKey(to='Poll.Opcion', on_delete=models.DO_NOTHING)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.user.rut + " --- (" + str(self.selected) + ") --- " + str(self.opcion.pregunta.tipo.pk) + ".- " +\
               self.opcion.pregunta.texto + ": " + self.opcion.texto

    class Meta:
        verbose_name = "Intermedia User Opcion"
        verbose_name_plural = "Intermedia Users Opciones"
