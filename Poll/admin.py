from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Sales)
admin.site.register(Poliza)
admin.site.register(SubPoliza)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(Tipo)
admin.site.register(PolizaOpcion)
admin.site.register(Dependencia)
admin.site.register(IntermediaDependenciaUser)

# admin.site.register(RiskManagement)
# admin.site.register(RiskPreventionPersonal)
