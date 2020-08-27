from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import *

from Poll.forms import LoginForm, ChangeProfileBSPoll, ChangeProfileBMPoll
from Home.models import UserGuiar, BusinessManager


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
    bs_form = ChangeProfileBSPoll()
    bm_form = ChangeProfileBMPoll(instance=manager)
    context = {'BS_profile': bs_form, 'BM_profile': bm_form, 'manager': manager}
    return render(request, 'Poll/mideturiesgo-page1.html', context)


class FormProfileBSPoll(FormView):
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
            user = UserGuiar.objects.get(rut=self.request.user.rut)
            user.name = f.cleaned_data['name_BS']
            user.rut = f.cleaned_data['rut_BS']
            user.seniority = f.cleaned_data['seniority']
            user.address = f.cleaned_data['address']
            user.city = f.cleaned_data['city']
            user.save()
            data = {
                'message': "Successfully submitted form data."
            }

            return JsonResponse(data)
        else:
            return response


class FormProfileMSPoll(UpdateView):
    model = BusinessManager
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
            form.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response



