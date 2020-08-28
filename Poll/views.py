from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import *

from Poll.forms import LoginForm, ChangeProfileBSPoll, ChangeProfileBMPoll, ChangeSaleFrom, QuantityEmpForm, ProcessForm
from Home.models import UserGuiar, BusinessManager, ProcessBusiness


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    login_form = LoginForm()
    context = {'form': login_form}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['rut']
            password = login_form.cleaned_data['password']

            user = authenticate(rut=username, password=password)

            if user:
                login(request, user)
                return render(request, 'Poll/profile.html')
            else:
                return render(request, 'Poll/login.html', context)
    return render(request, 'Poll/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    user = UserGuiar.objects.get(rut=request.user.rut)
    return render(request, 'Poll/profile.html', {'user': user})


def view_welcome(request):
    return render(request, 'Poll/welcome.html')


def poll_view(request):
    manager = UserGuiar.objects.get(rut=request.user).manager
    bs_form = ChangeProfileBSPoll(instance=request.user)
    bm_form = ChangeProfileBMPoll()
    sale_form = ChangeSaleFrom(instance=request.user)
    quantityEmp_form = QuantityEmpForm(instance=request.user)
    process_form = ProcessForm(instance=request.user)
    user = UserGuiar.objects.get(rut=request.user.rut)
    context = {
        'BS_profile': bs_form,
        'BM_profile': bm_form,
        'manager': manager,
        'sale_form': sale_form,
        'quantityEmp_form': quantityEmp_form,
        'process_form': process_form,
        'user': user
    }
    if request.method == "POST":
        process_form = ProcessForm(request.POST, instance=request.user)
        if process_form.is_valid():
            process_form.save()
            return render(request, 'Poll/mideturiesgo_page2.html')
    return render(request, 'Poll/mideturiesgo-page1.html', context)


def poll_risk(request):
    return render(request, 'Poll/mideturiesgo-page2.html')


class FormProfileBSPoll(UpdateView):
    model = UserGuiar
    form_class = ChangeProfileBSPoll
    template_name = 'Poll/forms/form_personal_BS.html'
    success_url = '/form-success/'

    def form_invalid(self, f):
        response = super(FormProfileBSPoll, self).form_invalid(f)
        if self.request.is_ajax():
            return JsonResponse(f.errors, status=400)
        else:
            return response

    def form_valid(self, f):
        response = super(FormProfileBSPoll, self).form_valid(f)
        if self.request.is_ajax():
            f.save()
            data = {
                'message': "Successfully submitted form data."
            }

            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = UserGuiar.objects.get(rut=self.request.user.rut)
        return obj


class FormProfileMSPoll(FormView):
    form_class = ChangeProfileBMPoll
    template_name = 'Poll/forms/form_personal_BM.html'
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(FormProfileMSPoll, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(FormProfileMSPoll, self).form_valid(form)
        if self.request.is_ajax():
            user = UserGuiar.objects.get(rut=self.request.user.rut)
            manager = user.manager
            manager.rut_bm = form.cleaned_data['rut_bm']
            manager.fullname = form.cleaned_data['fullname']
            manager.email = form.cleaned_data['email']
            manager.phone = form.cleaned_data['phone']
            manager.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response


class FormSalesPoll(UpdateView):
    model = UserGuiar
    form_class = ChangeSaleFrom
    template_name = 'Poll/forms/form_sale.html'
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(FormSalesPoll, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(FormSalesPoll, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = UserGuiar.objects.get(rut=self.request.user.rut)
        return obj


class FormQuantityPoll(UpdateView):
    model = UserGuiar
    form_class = QuantityEmpForm
    template_name = 'Poll/forms/form_dotacion.html'
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(FormQuantityPoll, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(FormQuantityPoll, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = UserGuiar.objects.get(rut=self.request.user.rut)
        return obj


class FormProcessPoll(UpdateView):
    model = UserGuiar
    form_class = ProcessForm
    template_name = 'Poll/forms/form_process.html'
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(FormProcessPoll, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(FormProcessPoll, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            type_process = []
            user = UserGuiar.objects.get(rut=self.request.user.rut)
            process = ProcessBusiness.objects.all()
            for e in process:
                if e in user.process.all():
                    type_process.append(e.title)
            print(type_process)
            data = {
                'message': "Successfully submitted form data.",
                'array': type_process,
            }
            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = UserGuiar.objects.get(rut=self.request.user.rut)
        return obj
