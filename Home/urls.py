from django.urls import path

from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.register_view, name='signUp')
]
