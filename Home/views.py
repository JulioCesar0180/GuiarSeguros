from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from GuiarSeguros import settings
from .models import BusinessManager, UserGuiar, RecoveryTokens
from .forms import CreateManagerForm, CreateUserForm, PasswordResetFormGS, SetPasswordFormGS, CreateRecuperarForm,\
    TokenForm, NewPasswordForm

from .utils import validate_rut

from django.core.mail import EmailMessage

import random
import string


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def home(request):
    return render(request, 'Home/home.html')


def view_register_manager(request):
    form_user = CreateUserForm()
    form_manager = CreateManagerForm()
    if request.is_ajax and request.method == "POST":
        form_user = CreateUserForm(request.POST)
        form_manager = CreateManagerForm(request.POST)
        if form_user.is_valid() and form_manager.is_valid() and validate_rut(form_manager.cleaned_data['rut_bm'])\
                and validate_rut(form_user.cleaned_data['rut']):
            instance_bm = form_manager.save(commit=False)
            instance_user = form_user.save(commit=False)
            
            instance_bm.rut_bm = instance_bm.rut_bm.upper()
            instance_bm.rut_bm = instance_bm.rut_bm.replace(".", "")
            
            instance_user.rut = instance_user.rut.upper()
            instance_user.rut = instance_user.rut.replace(".", "")
            
            instance_bm.save()
            instance_user.manager_id = instance_bm.id
            instance_user.save()

            user_query = UserGuiar.objects.get(rut=instance_user.rut)
            user_query.email_manager = form_manager.cleaned_data['email']
            user_manager = BusinessManager.objects.get(rut_bm=instance_bm.rut_bm)
            user_query.manager = user_manager
            subject = 'Bienvenido a Guiar Consultores'
            message = 'a'
            email_from = settings.EMAIL_HOST_USER
            email_to = [user_query.email_manager,]
            send_mail(subject, message, email_from, email_to)
            user_query.save()

            user = authenticate(rut=instance_user.rut, password=form_user.cleaned_data['password1'])
            print(user)
            if user:
                login(request, user)
                return redirect('profile')
        else:
            print("Ha ocurrido un error")
            messages.error(request, "Error")
            # return JsonResponse({'status': 'error', 'mensaje_user': form_user.errors, 'mensaje_bm': form_manager.errors}, status=400)
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


# Por hacer: Generar la tabla con los token e ids
def recuperar_password(request):
    form_recuperar = CreateRecuperarForm()
    context = {'form_recuperar': form_recuperar}
    if request.is_ajax and request.method == 'POST':
        form_recuperar = CreateRecuperarForm(request.POST)
        if form_recuperar.is_valid():
            if BusinessManager.objects.filter(email=form_recuperar.cleaned_data['email']).exists():
                correo = form_recuperar.cleaned_data['email']
                recovery_token = RecoveryTokens.objects.get_or_create(email=correo)
                token = get_random_string(8)
                recovery_token[0].token = token
                recovery_token[0].save()
                merge_data = {
                    'protocol': "https", 'domain': "guiarseguros.cl",
                    'token': token
                }
                subject = 'Recuperar contraseña'
                message = render_to_string('Home/auth_reset_password/password_reset_email.html', merge_data)
                email_from = settings.EMAIL_HOST_USER
                email_to = [correo, ]
                mensaje = EmailMessage(
                    subject,
                    message,
                    email_from,
                    email_to,
                )
                mensaje.content_subtype = "html"
                mensaje.send()
                return JsonResponse({"status": "Correcto",
                                     "mensaje": "Se ha enviado un mensaje con los pasos para recuperar su contraseña."})
            else:
                return JsonResponse({"status": "Fracaso", "mensaje": "Correo no encontrado"})
        else: 
            return JsonResponse({"status": "Fracaso", "mensaje": "Correo no encontrado"})
    return render(request, 'Home/new_recovery/recuperar_password.html', context)


def token_recovery(request):
    token_form = TokenForm()
    password_form = NewPasswordForm()
    context = {'token_form': token_form, 'password_form': password_form}
    if request.is_ajax and request.method == 'POST':
        token_form = TokenForm(request.POST)
        password_form = NewPasswordForm(request.POST)
        if token_form.is_valid() and password_form.is_valid():
            password1 = password_form.cleaned_data['new_password1']
            password2 = password_form.cleaned_data['new_password2']
            print()
            if password1 == password2:
                if RecoveryTokens.objects.filter(token=token_form.cleaned_data['token']).exists():
                    token = token_form.cleaned_data['token']
                    recovery_token = RecoveryTokens.objects.get_or_create(token=token)
                    user_manager = BusinessManager.objects.get(email=recovery_token[0].email)
                    user_guiar = UserGuiar.objects.get(manager_id=user_manager.id)
                    user_guiar.password = make_password(password1)
                    user_guiar.save()
                    subject = 'Contraseña actualizada correctamente'
                    message = 'Hemos realizado el cambio de su contraseña, proceda a iniciar sesión en Guiar Seguros'
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [user_manager.email, ]
                    mensaje = EmailMessage(
                        subject,
                        message,
                        email_from,
                        email_to,
                    )
                    mensaje.content_subtype = "html"
                    mensaje.send()
                    recovery_token[0].delete()
                    return JsonResponse({'url': 'mideturiesgo'})
                else: 
                    return JsonResponse({"status": "Error", "mensaje": "Código no encontrado."}, status=400)
            else:
                return JsonResponse({"status": "Error", "mensaje": "Contraseñas no son iguales"}, status=400)
        else:
            return JsonResponse({"status": "Error", "mensaje": "Código no encontrado."}, status=400)
    return render(request, 'Home/new_recovery/token_recovery.html', context)


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
