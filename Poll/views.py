from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import *

from Poll.forms import *
from Poll.models import *
from Home.models import UserGuiar, BusinessManager, ProcessBusiness, DotacionInfo
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
    formManager = ChangeProfileBMPoll(instance=manager)
    return render(request, 'Poll/profile.html', {'user': user, 'manager': manager, 'formManager': formManager})


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


class UpdateManagerView(UpdateView):
    model = BusinessManager
    form_class = ChangeProfileBMPoll


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
    for pol in polizas:
        desgloce.append([pol.name, 0, 0, pol.id])
    # Este codigo no funcionara si una poliza es eliminada, en tal caso habria que buscar entre las polizas la que
    # coincida con opcion.poliza.pk obteniendo su posicion y utilizando este valor en vez de la referencia directa
    # En esta parte si "Responsabilidad Civil de Empresa" no es la primera poliza en la tabla, entonces esto dejara de
    # funcionar, en tal caso habria que buscar el indice en el que se encuentra esta poliza o su equivalente
    for opcion in TransportProcess.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_transport
        desgloce[0][1] += opcion.ri_transport
        maximo += opcion.ri_transport
    for opcion in ManufactureProcess.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_manufacture
        desgloce[0][1] += opcion.ri_manufacture
        maximo += opcion.ri_manufacture
    for opcion in BuildingProcess.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_building
        desgloce[0][1] += opcion.ri_building
        maximo += opcion.ri_building
    for opcion in GeneralServicesProcess.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_service
        desgloce[0][1] += opcion.ri_service
        maximo += opcion.ri_service
    for opcion in ExplosiveControl.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_explosive
        desgloce[0][1] += opcion.ri_explosive
        maximo += opcion.ri_explosive
    for opcion in SubstanceControl.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_substance
        desgloce[0][1] += opcion.ri_substance
        maximo += opcion.ri_substance
    for opcion in ElectricityControl.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_electricity
        desgloce[0][1] += opcion.ri_electricity
        maximo += opcion.ri_electricity
    for opcion in HeightControl.objects.all():
        pos = opcion.poliza.pk - 1
        if pos != 0:
            desgloce[pos][1] += opcion.ri_height
        desgloce[0][1] += opcion.ri_height
        maximo += opcion.ri_height
    max = 0
    for opcion in ExplosiveConfirmed.objects.all():
        if opcion.value_ri_explosive > max:
            max = opcion.value_ri_explosive
    desgloce[0][1] += max
    maximo += max
    max = 0
    for opcion in SubstanceConfirmed.objects.all():
        if opcion.value_ri_substance > max:
            max = opcion.value_ri_substance
    desgloce[0][1] += max
    maximo += max
    max = 0
    for opcion in ElectricityConfirmed.objects.all():
        if opcion.value_ri_electricity > max:
            max = opcion.value_ri_electricity
    desgloce[0][1] += max
    maximo += max
    max = 0
    for opcion in HeightConfirmed.objects.all():
        if opcion.value_ri_height > max:
            max = opcion.value_ri_height
    desgloce[0][1] += max
    maximo += max
    # Se obtiene el usuario del cual se lee la informacion
    user = UserGuiar.objects.get(rut=pk)

    dotaciones = DotacionInfo.objects.all()
    cantidades = []
    cantidades.clear()
    # Aqui se asigna el codigo de las dotaciones a cada campo. Esto significa que si se cambia el codigo en la BD, esto
    # dejara de funcionar, por lo cual el codigo en si no debe ser modificado y quedara oculto en el admin al final
    cantidades.append([user.n_emp_hired, "DOT1"])
    cantidades.append([user.n_cont_emp, "DOT2"])
    cantidades.append([user.n_veh_com_light, "DOT3"])
    cantidades.append([user.n_veh_com_cont, "DOT4"])
    cantidades.append([user.n_veh_com_heavy, "DOT5"])
    cantidades.append([user.n_veh_com_heavy_cont, "DOT6"])
    cantidades.append([user.n_mach_heavy, "DOT7"])
    cantidades.append([user.n_mach_heavy_cont, "DOT8"])
    for dot in dotaciones:
        pos = dot.poliza.pk - 1
        codigo = dot.cod
        cant = 0
        for cantidad in cantidades:
            if cantidad[1] == codigo:
                cant = cantidad[0]
                break
        if dot.min_value > dot.max_value:
            if cant > dot.min_value:
                if pos != 0:
                    desgloce[pos][2] += dot.ri_value * dot.min_value
                desgloce[0][2] += dot.ri_value * dot.min_value
                total += dot.ri_value * dot.min_value
            if pos != 0:
                desgloce[pos][1] += dot.ri_value * dot.min_value
            desgloce[0][1] += dot.ri_value * dot.min_value
            maximo += dot.ri_value * dot.min_value
        else:
            if cant >= dot.min_value:
                if cant < dot.max_value:
                    if pos != 0:
                        desgloce[pos][2] += dot.ri_value * cant
                    desgloce[0][2] += dot.ri_value * cant
                    total += dot.ri_value * cant

    # Se lleva la cuenta de los resultados de Transporte
    for proceso in user.transport.all():
        total += proceso.ri_transport
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_transport
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_transport

    # Se lleva la cuenta de los resultados de Construccion
    for proceso in user.building.all():
        total += proceso.ri_building
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_building
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_building

    # Se lleva la cuenta de los resultados de Manufactura
    for proceso in user.manufacture.all():
        total += proceso.ri_manufacture
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_manufacture
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_manufacture

    # Se lleva la cuenta de los resultados de Servicios Generales
    for proceso in user.general_services.all():
        total += proceso.ri_service
        for des in desgloce:
            if proceso.poliza.id == des[3]:
                des[2] += proceso.ri_service
                if not proceso.poliza.id == 1:
                    desgloce[0][2] += proceso.ri_service

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
    print("este es el maximo", maximo)

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