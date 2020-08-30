from django.urls import path

from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.RegisterManager.as_view(), name='signUp')
]
