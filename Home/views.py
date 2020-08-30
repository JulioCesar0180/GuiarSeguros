from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from .models import BusinessManager
from .forms import CreateManagerForm


def home(request):
    return render(request, 'Home/home.html')


def register_view(request):
    return render(request, 'Home/signUp.html')


class RegisterManager(CreateView):
    model = BusinessManager
    form_class = CreateManagerForm
    template_name = 'Home/forms/manager_create_form.html'


class PasswordResetViewGS(PasswordResetView):
    template_name = 'Home/password_reset_form.html'

