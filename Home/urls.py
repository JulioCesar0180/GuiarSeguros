from django.urls import path

from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.view_register_manager, name='signUp'),
    path('sigUp-error', views.view_register_manager_error, name='manager_error')
]
