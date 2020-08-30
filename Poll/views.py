from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

# Create your views here.
from django.views.generic import *

from Poll.forms import *
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


@login_required
def profile_view(request):
    user = UserGuiar.objects.get(rut=request.user.rut)
    return render(request, 'Poll/profile.html', {'user': user})


@login_required
def view_welcome(request):
    return render(request, 'Poll/welcome.html')


@login_required
def view_form_profile_bs(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ChangeProfileBSPoll(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ChangeProfileBSPoll(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-manager', user.pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_personal_BS.html', context)


@login_required
def view_form_profile_bm(request, pk):
    manager = BusinessManager.objects.get(userguiar__rut=pk)
    form = ChangeProfileBMPoll(instance=manager)
    context = {'manager': manager, 'form': form}
    if request.method == "POST":
        form = ChangeProfileBMPoll(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('poll-sales', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_personal_BM.html', context)


@login_required
def view_form_sales(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ChangeSaleFrom(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ChangeSaleFrom(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-quantity', user.pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_sale.html', context)


@login_required
def view_form_quantity(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = QuantityEmpForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = QuantityEmpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-process', user.pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_dotacion.html', context)


@login_required
def view_form_process(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-transport', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_process.html', context)


@login_required
def view_transport_process(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    process = ProcessBusiness.objects.get(title="Transporte")
    if process not in user.process.all():
        return redirect('poll-manufacture', pk)

    form = TransportProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = TransportProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-manufacture', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_transport.html', context)


@login_required
def view_manufacture_process(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    process = ProcessBusiness.objects.get(title="Manufactura")
    if process not in user.process.all():
        return redirect('poll-building', pk)

    form = ManufactureProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ManufactureProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-building', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_manufacture.html', context)


@login_required
def view_building_process(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    process = ProcessBusiness.objects.get(title="Construcción")
    if process not in user.process.all():
        return redirect('poll-services', pk)

    form = BuildingProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = BuildingProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-services', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_building.html', context)


@login_required
def view_services_process(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    process = ProcessBusiness.objects.get(title="Servicios Generales")
    if process not in user.process.all():
        return redirect('poll-control-risk', pk)

    form = GeneralServiceForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = GeneralServiceForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-control-risk', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_services.html', context)


@login_required
def view_control_risk(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ControlRiskForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ControlRiskForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-prevent-risk', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_risk.html', context)


@login_required
def view_prevent_risk(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = PreventRiskForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = PreventRiskForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-explosive', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_prevnet_risk.html', context)


@login_required
def view_confirmed_control_explosive(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ExplosiveConfirmedForm(instance=user)
    if request.method == "POST":
        form = ExplosiveConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.explosive_confirmed.option_explosive == "Sí":
                return redirect('poll-explosive', pk)
            else:
                return redirect('poll-confirmed-electricity', pk)
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_explosive.html', context)


@login_required
def view_control_explosive(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ExplosiveControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ExplosiveControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-electricity', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_explosives.html', context)


@login_required
def view_confirmed_control_electricity(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ElectricityConfirmedForm(instance=user)
    if request.method == "POST":
        form = ElectricityConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.electricity_confirmed.option_electricity == "Sí":
                return redirect('poll-electricity', pk)
            else:
                return redirect('poll-confirmed-substance', pk)
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_electricity.html', context)


@login_required
def view_control_electricity(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = ElectricityControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ElectricityControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-substance', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_electricity.html', context)


@login_required
def view_confirmed_substances(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = SubstancesConfirmedForm(instance=user)
    if request.method == "POST":
        form = SubstancesConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.substance_confirmed.option_substance == "Sí":
                return redirect('poll-substance', pk)
            else:
                return redirect('poll-confirmed-height', pk)
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_substance.html', context)


@login_required
def view_control_substances(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = SubstanceControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = SubstanceControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-height', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_substance.html', context)


@login_required
def view_confirmed_height(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = HeightConfirmedForm(instance=user)
    if request.method == "POST":
        form = HeightConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.height_confirmed.option_height == "Sí":
                return redirect('poll-height', pk)
            else:
                return redirect('poll-results', pk)
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_height.html', context)


@login_required
def view_control_height(request, pk):
    user = UserGuiar.objects.get(rut=pk)
    form = HeightControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = HeightControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-results', pk)
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_height.html', context)


@login_required
def view_results(request, pk):
    # [Nombre de la poliza, maximo puntaje, puntaje obtenido, id de la Poliza]
    desgloce = []
    # Resultado global independiente de las polizas
    total = 0
    user = UserGuiar.objects.get(rut=pk)
    for proceso in user.transport.all():
        print(proceso.ri_transport)
    # for poliza in TablaPoliza.objects.all():
    #         desgloce.append([poliza.nombre_poliza,0,0,poliza.id])

    return HttpResponse("Results")
