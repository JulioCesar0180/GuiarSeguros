from django.db import models

# Create your models here.


class Sales(models.Model):
    title = models.CharField(max_length=100)
    amortiguador = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        # return self.title + " ; " + str(self.amortiguador)
        return self.title

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


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


class PolizaOpcion(models.Model):
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)
    opcion = models.ForeignKey('Opcion', models.DO_NOTHING, null=True, blank=True)
    riesgo = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.poliza.name + " --- " + str(self.opcion.pk)

    class Meta:
        verbose_name = "Intermedia Poliza-Opcion"
        verbose_name_plural = "Intermedia Polizas-Opciones"


class PolizaDependencia(models.Model):
    poliza = models.ForeignKey('SubPoliza', models.DO_NOTHING, null=True, blank=True)
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.poliza.name + " --- " + str(self.dependencia.pk)

    class Meta:
        verbose_name = "Intermedia Poliza-Dependencia"
        verbose_name_plural = "Intermedia Polizas-Dependencias"


class Pregunta(models.Model):
    tipo = models.ForeignKey('Tipo', models.DO_NOTHING, null=True, blank=True)
    texto = models.CharField(max_length=200)
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING, null=True, blank=True)
    # abreviacion = models.CharField(max_length=50)

    def __str__(self):
        return str(self.tipo.pk) + " - " + self.texto

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"


class Opcion(models.Model):
    texto = models.CharField(max_length=200)
    riesgo = models.DecimalField(max_digits=5, decimal_places=2)
    pregunta = models.ForeignKey('Pregunta', models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.texto
        # return str(self.pregunta.tipo.pk)+": "+self.pregunta.texto+" --- "+self.texto+" ("+str(self.riesgo)+")"
        # return str(self.pregunta.tipo.pk)+": "+self.pregunta.abreviacion+" --- "+self.texto+" ("+str(self.riesgo)+")"

    class Meta:
        verbose_name = "Opcion"
        verbose_name_plural = "Opciones"


class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Pregunta"
        verbose_name_plural = "Tipos de Preguntas"


class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    riesgo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tipo = models.CharField(choices=[("1", "Procesos"), ("2", "Actividades")], max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"


class IntermediaDependenciaUser(models.Model):
    user = models.ForeignKey(to='Home.UserGuiar', on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.user.rut + " --- " + self.dependencia.nombre + " (" + str(self.selected) + ")"

    class Meta:
        verbose_name = "Intermedia User Dependencia"
        verbose_name_plural = "Intermedia Users Dependencias"
