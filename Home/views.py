from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import BusinessManager, UserGuiar
from .forms import CreateManagerForm


def home(request):
    return render(request, 'Home/home.html')


def view_register_manager(request):
    form = CreateManagerForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Home/home.html')
        else:
            manager = BusinessManager.objects.get(rut_bm=request.POST['rut_bm'])
            print(manager)
            user = UserGuiar.objects.get(manager_id=manager.pk)
            context = {'manager': manager.fullname}
            messages.add_message(request, messages.INFO, manager.rut_bm)
            return redirect('manager_error')
    return render(request, 'Home/forms/manager_create_form.html', context)


def view_register_manager_error(request):
    msj = get_messages(request)
    rut_bm = None
    for i in msj:
        rut_bm = i
    manager = get_object_or_404(BusinessManager, rut_bm=rut_bm)
    return render(request, 'Home/forms/manager_create_error.html')


class PasswordResetViewGS(PasswordResetView):
    template_name = 'Home/password_reset_form.html'

