from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'Home/home.html')


def register_view(request):
    return render(request, 'Home/signUp.html')


class PasswordResetViewGS(PasswordResetView):
    template_name = 'Home/password_reset_form.html'

