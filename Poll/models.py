from django.db import models

# Create your models here.


class Sales(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class ProcessBusiness(models.Model):
    title = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Proceso Empresarial"
        verbose_name_plural = "Procesos Empresariales"


class TransportProcess(models.Model):
    option_transport = models.CharField(max_length=100)
    ri_transport = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.option_transport

    class Meta:
        verbose_name = "Proceso de Transporte"
        verbose_name_plural = "Procesos de Transportes"


class ManufactureProcess(models.Model):
    option_manufacture = models.CharField(max_length=100)
    ri_manufacture = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.option_manufacture

    class Meta:
        verbose_name = "Proceso de Manufactura"
        verbose_name_plural = "Procesos de Manufacturas"


class BuildingProcess(models.Model):
    option_building = models.CharField(max_length=100)
    ri_building = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.option_building

    class Meta:
        verbose_name = "Proceso de Contrucción"
        verbose_name_plural = "Procesos de Construccion"


class GeneralServicesProcess(models.Model):
    option_service = models.CharField(max_length=100)
    ri_service = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.option_service

    class Meta:
        verbose_name = "Proceso de Servicio General"
        verbose_name_plural = "Procesos de Servicios Generales"


class RiskManagement(models.Model):
    option_risk = models.CharField(max_length=100)
    ri_risk = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_risk

    class Meta:
        verbose_name = "Manejo de Riesgo"
        verbose_name_plural = "Manejo de Riesgos"


class RiskPreventionPersonal(models.Model):
    option_prevent = models.CharField(max_length=100)
    ri_prevent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_prevent

    class Meta:
        verbose_name = "Prevesión de Riesgo"
        verbose_name_plural = "Prevension de Riesgos"


class ExplosiveControl(models.Model):
    explosive_control = models.CharField(max_length=255)
    ri_explosive = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.explosive_control

    class Meta:
        verbose_name = "Manejo de Explosivo"
        verbose_name_plural = "Manejo de Explosivos"


class ElectricityControl(models.Model):
    electricity_control = models.CharField(max_length=255)
    ri_electricity = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.electricity_control

    class Meta:
        verbose_name = "Manejo de riesgo eléctrico"
        verbose_name_plural = "Manejo de riesgos eléctricos"


class SubstanceControl(models.Model):
    substance_control = models.CharField(max_length=255)
    ri_substance = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.substance_control

    class Meta:
        verbose_name = "Manejo de Sustancia Peligrosa"
        verbose_name_plural = "Manejo de Sustancias Peligrosas"


class HeightControl(models.Model):
    height_control = models.CharField(max_length=255)
    ri_height = models.DecimalField(max_digits=5, decimal_places=2)
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.height_control

    class Meta:
        verbose_name = "Manejo de Riesgo en Altura"
        verbose_name_plural = "Manejo de Riesgos en Altura"


class Poliza(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Poliza"
        verbose_name_plural = "Polizas"


class SubPoliza(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()
    categoria = models.ForeignKey('Poliza', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.categoria.name + " --- " + self.name

    class Meta:
        verbose_name = "Sub-Poliza"
        verbose_name_plural = "Sub-Polizas"


class ExplosiveConfirmed(models.Model):
    option_explosive = models.CharField(max_length=10)
    value_ri_explosive = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_explosive

    class Meta:
        verbose_name = "Confirmación de Riesgo Explosivo"
        verbose_name_plural = "Confirmación de Riesgos Explosivos"


class ElectricityConfirmed(models.Model):
    option_electricity = models.CharField(max_length=10)
    value_ri_electricity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_electricity

    class Meta:
        verbose_name = "Confirmación de Riesgo Electricos"
        verbose_name_plural = "Confirmación Riesgos Electricos"


class SubstanceConfirmed(models.Model):
    option_substance = models.CharField(max_length=10)
    value_ri_substance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_substance

    class Meta:
        verbose_name = "Confirmación de Riesgo de Sustancia Peligrosa"
        verbose_name_plural = "Confirmación de Riesgos de Sustancias Peligrosas"


class HeightConfirmed(models.Model):
    option_height = models.CharField(max_length=10)
    value_ri_height = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.option_height

    class Meta:
        verbose_name = "Confirmación de Riesgo en Altura"
        verbose_name_plural = "Confirmación de Riesgos en Altura"
