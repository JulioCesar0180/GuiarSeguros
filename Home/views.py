from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView
from django.contrib.messages import get_messages
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import CreateView

from GuiarSeguros import settings
from .models import BusinessManager, UserGuiar
from .forms import CreateManagerForm, CreateUserForm, PasswordResetFormGS, SetPasswordFormGS, UserChangePassword

from .utils import validate_rut

def home(request):
    return render(request, 'Home/home.html')


def view_register_manager(request):
    form_user = CreateUserForm()
    form_manager = CreateManagerForm()
    if request.method == "POST":
        form_user = CreateUserForm(request.POST)
        form_manager = CreateManagerForm(request.POST)
        if form_user.is_valid() and form_manager.is_valid() and validate_rut(form_manager.cleaned_data['rut_bm'])\
                and validate_rut(form_user.cleaned_data['rut']):
            form_manager.save()
            form_user.save()
            user_query = UserGuiar.objects.get(rut=form_user.cleaned_data['rut'])
            user_query.email_manager = form_manager.cleaned_data['email']
            user_manager = BusinessManager.objects.get(rut_bm=form_manager.cleaned_data['rut_bm'])
            user_query.manager = user_manager
            subject = 'Bienvenido a Guiar Consultores'
            message = 'a'
            email_from = settings.EMAIL_HOST_USER
            email_to = [user_query.email_manager,]
            send_mail(subject, message, email_from, email_to)
            user_query.save()

            user = authenticate(rut=form_user.cleaned_data['rut'], password=form_user.cleaned_data['password1'])
            print(user)
            if user:
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, "Error")
    context = {'form_user': form_user, 'form_manager': form_manager}
    return render(request, 'Home/forms/form_signup.html', context)


class PasswordResetViewGS(PasswordResetView):
    template_name = 'Home/auth_reset_password/password_reset.html'
    form_class = PasswordResetFormGS
    success_url = reverse_lazy('recovery_done')
    email_template_name = 'Home/auth_reset_password/password_reset_email.html'
    html_email_template_name = 'Home/auth_reset_password/password_reset_email.html'
    from_email = settings.EMAIL_HOST_USER


class PasswordResetDoneViewGS(PasswordResetDoneView):
    template_name = 'Home/auth_reset_password/password_reset_done.html'


class PasswordResetConfirmViewGS(PasswordResetConfirmView):
    template_name = 'Home/auth_reset_password/password_reset_confirm.html'
    form_class = SetPasswordFormGS
    success_url = reverse_lazy('recovery-complete')


class PasswordResetCompleteViewGS(PasswordResetCompleteView):
    template_name = 'Home/auth_reset_password/password_reset_complete.html'


def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Home/auth_reset_password/password_change.html', {
        'form': form
    })
