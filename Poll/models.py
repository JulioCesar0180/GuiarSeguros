from django.db import models

# Create your models here.


class Sales(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProcessBusiness(models.Model):
    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class TransportProcess(models.Model):
    option_transport = models.CharField(max_length=100)
    ri_transport = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.option_transport


class ManufactureProcess(models.Model):
    option_manufacture = models.CharField(max_length=100)
    ri_manufacture = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.option_manufacture


class BuildingProcess(models.Model):
    option_building = models.CharField(max_length=100)
    ri_building = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.option_building


class GeneralServicesProcess(models.Model):
    option_service = models.CharField(max_length=100)
    ri_service = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.option_service


class RiskManagement(models.Model):
    option_risk = models.CharField(max_length=100)
    ri_risk = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_risk


class RiskPreventionPersonal(models.Model):
    option_prevent = models.CharField(max_length=100)
    ri_prevent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_prevent


class ExplosiveControl(models.Model):
    explosive_control = models.CharField(max_length=255)
    ri_explosive = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.explosive_control


class ElectricityControl(models.Model):
    electricity_control = models.CharField(max_length=255)
    ri_electricity = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.electricity_control


class SubstanceControl(models.Model):
    substance_control = models.CharField(max_length=255)
    ri_substance = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.substance_control


class HeightControl(models.Model):
    height_control = models.CharField(max_length=255)
    ri_height = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('Poliza', models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.height_control


class Poliza(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class ExplosiveConfirmed(models.Model):
    option_explosive = models.CharField(max_length=10)
    value_ri_explosive = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_explosive


class ElectricityConfirmed(models.Model):
    option_electricity = models.CharField(max_length=10)
    value_ri_electricity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_electricity


class SubstanceConfirmed(models.Model):
    option_substance = models.CharField(max_length=10)
    value_ri_substance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_substance


class HeightConfirmed(models.Model):
    option_height = models.CharField(max_length=10)
    value_ri_height = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_height
