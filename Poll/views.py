from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import *

from Poll.forms import *
from Poll.models import Poliza
from Home.models import UserGuiar, BusinessManager, ProcessBusiness
from GuiarSeguros.utils import render_to_pdf

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
    manager = BusinessManager.objects.get(rut_bm=user.manager.rut_bm)
    return render(request, 'Poll/profile.html', {'user': user, 'manager': manager})


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
        user.transport.clear()
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
        user.manufacture.clear()
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
        user.building.clear()
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
        user.general_services.clear()
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
                user.explosive_control.clear()
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
                user.electricity_control.clear()
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
                user.substance_control.clear()
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
                user.height_control.clear()
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
    desgloce.clear()
    # Resultado global independiente de las polizas
    total = 0
    # Maximo y Minimo valor obtenible en la encuesta (para ajustar la representacion grafica)
    maximo = 0
    minimo = 0
    # Se generan las categorias a considerar en los resultados
    polizas = Poliza.objects.all()
    i = 0
    index = 0
    index1 = 0
    index2 = 0
    index3 = 0
    index4 = 0
    for pol in polizas:
        desgloce.append([pol.name, 0, 0, pol.id])
        # Se obtiene la posicion de la poliza de accidentes personales
        if pol.name == "Accidentes Personales":
            index = i
        if pol.name == "Equipos Móviles":
            index1 = i
        if pol.name == "Vehículos Comerciales Livianos":
            index2 = i
        if pol.name == "Vehículos Comerciales Pesados":
            index3 = i
        if pol.name == "Transporte Terrestre":
            index4 = i
        i += 1

    # Se obtiene el usuario del cual se lee la informacion
    user = UserGuiar.objects.get(rut=pk)

    emp = user.n_cont_emp
    if emp < 50:
        desgloce[index][2] += 1 * emp
        if index != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 50 <= emp < 125:
        desgloce[index][2] += 2 * emp
        if index != 0:
            desgloce[0][2] += 2 * emp
        total += 2 * emp
    elif 125 <= emp < 200:
        desgloce[index][2] += 3 * emp
        if index != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    else:
        desgloce[index][2] += 4 * 200
        if index != 0:
            desgloce[0][2] += 4 * 200
        total += 4 * 200
    maximo += 4 * 200
    if index != 0:
        desgloce[index][1] += 4 * 200
    desgloce[0][1] += 4 * 200
    # TODO: Corroborar si este campo es de empleado propio de la empresa o contratista (lo mismo para el campo anterior)
    emp = user.n_emp_hired
    if emp < 50:
        desgloce[index][2] += 1 * emp
        if index != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 50 <= emp < 125:
        desgloce[index][2] += 2 * emp
        if index != 0:
            desgloce[0][2] += 2 * emp
        total += 2 * emp
    elif 125 <= emp < 200:
        desgloce[index][2] += 3 * emp
        if index != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    else:
        desgloce[index][2] += 5 * 200
        if index != 0:
            desgloce[0][2] += 5 * 200
        total += 5 * 200
    maximo += 5 * 200
    if index != 0:
        desgloce[index][1] += 5 * 200
    desgloce[0][1] += 5 * 200

    emp = user.n_veh_com_light
    if emp < 20:
        desgloce[index2][2] += 1 * emp
        if index2 != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 20 <= emp < 30:
        desgloce[index2][2] += 3 * emp
        if index2 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 30 <= emp < 40:
        desgloce[index2][2] += 5 * emp
        if index2 != 0:
            desgloce[0][2] += 5 * emp
        total += 5 * emp
    elif 40 <= emp < 50:
        desgloce[index2][2] += 6 * emp
        if index2 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    else:
        desgloce[index2][2] += 7 * 50
        if index2 != 0:
            desgloce[0][2] += 7 * 50
        total += 7 * 50
    maximo += 7 * 50
    if index != 0:
        desgloce[index2][1] += 7 * 50
    desgloce[index2][1] += 7 * 50

    emp = user.n_veh_com_cont
    if emp < 20:
        desgloce[index2][2] += 1 * emp
        if index2 != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 20 <= emp < 30:
        desgloce[index2][2] += 3 * emp
        if index2 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 30 <= emp < 40:
        desgloce[index2][2] += 5 * emp
        if index2 != 0:
            desgloce[0][2] += 5 * emp
        total += 5 * emp
    elif 40 <= emp < 50:
        desgloce[index2][2] += 6 * emp
        if index2 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    else:
        desgloce[index2][2] += 7 * 50
        if index2 != 0:
            desgloce[0][2] += 7 * 50
        total += 7 * 50
    maximo += 7 * 50
    if index != 0:
        desgloce[index2][1] += 7 * 50
    desgloce[0][1] += 7 * 50

    emp = user.n_veh_com_heavy
    if emp < 20:
        desgloce[index3][2] += 3 * emp
        if index3 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 20 <= emp < 30:
        desgloce[index3][2] += 6 * emp
        if index3 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    elif 30 <= emp < 40:
        desgloce[index3][2] += 9 * emp
        if index3 != 0:
            desgloce[0][2] += 9 * emp
        total += 9 * emp
    elif 40 <= emp < 50:
        desgloce[index3][2] += 12 * emp
        if index3 != 0:
            desgloce[0][2] += 12 * emp
        total += 12 * emp
    else:
        desgloce[index3][2] += 15 * 50
        if index3 != 0:
            desgloce[0][2] += 15 * 50
        total += 15 * 50
    maximo += 15 * 50
    if index != 0:
        desgloce[index3][1] += 15 * 50
    desgloce[0][1] += 15 * 50

    emp = user.n_veh_com_heavy_cont
    if emp < 20:
        desgloce[index3][2] += 3 * emp
        if index3 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 20 <= emp < 30:
        desgloce[index3][2] += 6 * emp
        if index3 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    elif 30 <= emp < 40:
        desgloce[index3][2] += 9 * emp
        if index3 != 0:
            desgloce[0][2] += 9 * emp
        total += 9 * emp
    elif 40 <= emp < 50:
        desgloce[index3][2] += 12 * emp
        if index3 != 0:
            desgloce[0][2] += 12 * emp
        total += 12 * emp
    else:
        desgloce[index3][2] += 15 * 50
        if index3 != 0:
            desgloce[0][2] += 15 * 50
        total += 15 * 50
    maximo += 15 * 50
    if index != 0:
        desgloce[index3][1] += 15 * 50
    desgloce[0][1] += 15 * 50

    emp = user.n_mach_heavy
    if emp < 20:
        desgloce[index1][2] += 1 * emp
        if index1 != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 20 <= emp < 30:
        desgloce[index1][2] += 3 * emp
        if index1 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 30 <= emp < 40:
        desgloce[index1][2] += 5 * emp
        if index1 != 0:
            desgloce[0][2] += 5 * emp
        total += 5 * emp
    elif 40 <= emp < 50:
        desgloce[index1][2] += 6 * emp
        if index1 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    else:
        desgloce[index1][2] += 7 * 50
        if index1 != 0:
            desgloce[0][2] += 7 * 50
        total += 7 * 50
    maximo += 7 * 50
    if index != 0:
        desgloce[index1][1] += 7 * 50
    desgloce[0][1] += 7 * 50

    emp = user.n_mach_heavy_cont
    if emp < 20:
        desgloce[index1][2] += 1 * emp
        if index1 != 0:
            desgloce[0][2] += 1 * emp
        total += 1 * emp
    elif 20 <= emp < 30:
        desgloce[index1][2] += 3 * emp
        if index1 != 0:
            desgloce[0][2] += 3 * emp
        total += 3 * emp
    elif 30 <= emp < 40:
        desgloce[index1][2] += 5 * emp
        if index1 != 0:
            desgloce[0][2] += 5 * emp
        total += 5 * emp
    elif 40 <= emp < 50:
        desgloce[index1][2] += 6 * emp
        if index1 != 0:
            desgloce[0][2] += 6 * emp
        total += 6 * emp
    else:
        desgloce[index1][2] += 7 * 50
        if index1 != 0:
            desgloce[0][2] += 7 * 50
        total += 7 * 50
    maximo += 7 * 50
    if index != 0:
        desgloce[index1][1] += 7 * 50
    desgloce[0][1] += 7 * 50

    # Se lleva la cuenta de los resultados de Transporte
    for proceso in user.transport.all():
        total += proceso.ri_transport
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_transport
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_transport
    # TODO: Agregar los verdaderos maximos desde este punto en adelante de manera automatica
    maximo += 18
    desgloce[index4][1] += 18
    desgloce[0][1] += 18

    # Se lleva la cuenta de los resultados de Construccion
    for proceso in user.building.all():
        total += proceso.ri_building
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_building
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_building
    maximo += 14
    desgloce[0][1] += 14
    # Se lleva la cuenta de los resultados de Manufactura
    for proceso in user.manufacture.all():
        total += proceso.ri_manufacture
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_manufacture
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_manufacture
    maximo += 12
    desgloce[0][1] += 12
    # Se lleva la cuenta de los resultados de Servicios Generales
    for proceso in user.general_services.all():
        total += proceso.ri_service
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_service
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_service
    maximo += 35
    desgloce[0][1] += 35

    # Se lleva la cuenta de los resultados de Manejo de Riesgo
    manejo_riesgo = user.risk_management.ri_risk
    print(manejo_riesgo)            
    # Se lleva la cuenta de los resultados de Prevencionista de Riesgo
    prevencionista = user.risk_prevent.ri_prevent
    print(prevencionista)

    # Se obtiene el total de amortiguacion de riesgo en %, aqui no hay un valor maximo que aumente el riesgo
    amortiguacion = (manejo_riesgo + prevencionista)/100

    # Se lleva la cuenta de los resultados de Explosivos
    riesgo = user.explosive_confirmed.value_ri_explosive
    if user.explosive_confirmed.option_explosive == "Sí":
        total += riesgo
        desgloce[0][2] += riesgo
        for proceso in user.explosive_control.all():
            total += proceso.ri_explosive
            for des in desgloce:
                if proceso.poliza.id == des[3]:
                    des[2] += proceso.ri_explosive
                    if not proceso.poliza.id == 1:
                        desgloce[0][2] += proceso.ri_explosive
    maximo += riesgo + 25
    desgloce[0][1] += riesgo + 25

    # Se lleva la cuenta de los resultados de Electricidad
    riesgo = user.electricity_confirmed.value_ri_electricity
    if user.electricity_confirmed.option_electricity == "Sí":
        total += riesgo
        desgloce[0][2] += riesgo
        for proceso in user.electricity_control.all():
            total += proceso.ri_electricity
            for des in desgloce:
                if proceso.poliza.id == des[3]:
                    des[2] += proceso.ri_electricity
                    if not proceso.poliza.id == 1:
                        desgloce[0][2] += proceso.ri_electricity
    maximo += riesgo + 25
    desgloce[0][1] += riesgo + 25

    # Se lleva la cuenta de los resultados de Sustancias Peligrosas
    riesgo = user.substance_confirmed.value_ri_substance
    if user.substance_confirmed.option_substance == "Sí":
        total += riesgo
        desgloce[0][2] += riesgo
        for proceso in user.substance_control.all():
            total += proceso.ri_substance
            for des in desgloce:
                if proceso.poliza.id == des[3]:
                    des[2] += proceso.ri_substance
                    if not proceso.poliza.id == 1:
                        desgloce[0][2] += proceso.ri_substance
    maximo += riesgo + 30
    desgloce[0][1] += riesgo + 30

    # Se lleva la cuenta de los resultados de Altura
    riesgo = user.height_confirmed.value_ri_height
    if user.height_confirmed.option_height == "Sí":
        total += riesgo
        desgloce[0][2] += riesgo
        for proceso in user.height_control.all():
            total += proceso.ri_height
            for des in desgloce:
                if proceso.poliza.id == des[3]:
                    des[2] += proceso.ri_height
                    if not proceso.poliza.id == 1:
                        desgloce[0][2] += proceso.ri_height
    maximo += riesgo + 20
    desgloce[0][1] += riesgo + 20

    for d in desgloce:
        d[2] = d[2] * (1 - amortiguacion)

    for d in desgloce:
        print(d[0], d[1], d[2], d[3])

    desgloce_ordenado = []
    desgloce_ordenado.clear()
    for des in desgloce:
        # Se filtran los resultados nulos
        if des[2] != 0:
            # Este nuevo arreglo tiene [Nombre Poliza, Maximo Poliza, Resultado Poliza, ID Poliza]
            desgloce_ordenado.append([des[0], des[1], round((des[2]/des[1])*100,2), des[3]])

    desgloce_ordenado.sort(key=lambda array: array[2], reverse=True)
    for d in desgloce_ordenado:
        print(d[0], d[1], d[2], d[3])

    res_por = ((total) / (maximo))
    res_img = (379 + 19) * res_por
    res_fin = (379 + 19) - res_img
    res_fin = int(res_fin)
    cuartil = (maximo) / 4

    if total < (cuartil):
        color = "VERDE"
    elif (cuartil) <= total < (2 * cuartil):
        color = "AMARILLO"
    elif (2 * cuartil) <= total <= (3 * cuartil):
        color = "ANARANJADO"
    else:
        color = "ROJO"

    return render(request, 'Poll/results.html',
                  {'maximo': maximo, 'minimo': minimo, 'total': total, 'res_fin': res_fin, 'color': color, 'desgloce': desgloce_ordenado})

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")