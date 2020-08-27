from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import UserGuiarCreationForm
# Register your models here.


@admin.register(UserGuiar)
class UserGuiarAdmin(UserAdmin):
    add_form = UserGuiarCreationForm
    model = UserGuiar
    list_display = ['rut', 'name', 'is_admin']
    list_filter = ['is_admin', 'name']
    ordering = ['rut']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rut', 'name', 'password1', 'password2',)
        }),
    )

    fieldsets = (
        (None, {'fields': ('rut', 'password')}),
        ('Datos de la empresa', {'fields': ('name', 'city', 'town', 'seniority')}),
        ('Datos del representante', {'fields': ('manager',)}),
        ('Ventas Anuales', {'fields': ('sales',)}),
        ('Dotación Empresa', {'fields': ('n_emp_hired', 'n_cont_emp', 'n_veh_com_light', 'n_veh_com_cont',
                                         'n_veh_com_heavy', 'n_veh_com_heavy_cont', 'n_mach_heavy', 'n_mach_heavy_cont')}),
        ('Procesos', {'fields': ('process',)}),
        ('Permisos', {'fields': ('is_admin',)})
    )


admin.site.register(BusinessManager)
admin.site.register(City)
admin.site.register(Town)
