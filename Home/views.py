from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import BusinessManager, UserGuiar
from .forms import CreateManagerForm, CreateUserForm


def home(request):
    return render(request, 'Home/home.html')


def view_register_manager(request):
    form_user = CreateUserForm()
    form_manager = CreateManagerForm()
    context = {'form_user': form_user, 'form_manager': form_manager}
    if request.method == "POST":
        form_user = CreateUserForm(request.POST)
        form_manager = CreateManagerForm(request.POST)
        print('manager: ', form_manager.is_valid(), 'user: ', form_user.is_valid())
        if form_user.is_valid() and form_manager.is_valid():
            form_manager.save()
            form_user.save()
            user_query = UserGuiar.objects.get(rut=form_user.cleaned_data['rut'])
            user_manager = BusinessManager.objects.get(rut_bm=form_manager.cleaned_data['rut_bm'])
            user_query.manager = user_manager
            user_query.save()

            user = authenticate(rut=form_user.cleaned_data['rut'], password=form_user.cleaned_data['password1'])
            print(user)
            if user:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, "Error")
    return render(request, 'Home/forms/form_signup.html', context)


def view_register_manager_error(request):
    msj = get_messages(request)
    rut_bm = None
    for i in msj:
        rut_bm = i
    manager = get_object_or_404(BusinessManager, rut_bm=rut_bm)
    return render(request, 'Home/forms/manager_create_error.html')


class PasswordResetViewGS(PasswordResetView):
    template_name = 'Home/password_reset_form.html'

