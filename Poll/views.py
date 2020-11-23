from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import *

from Poll.forms import *
from Poll.models import *
from Home.models import UserGuiar, BusinessManager, ProcessBusiness, Dotacion, DotacionEmpresarial, RangosDotacion,\
    IntermediaUserOpcion
#PDF
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template


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
                return redirect('profile')
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
    if user.is_admin:
        return redirect('/admin/')
    else:
        manager = BusinessManager.objects.get(rut_bm=user.manager.rut_bm)
        formManager = ChangeProfileBMPoll(instance=manager)
        formUser = ChangeProfileBSPoll(instance=user)
        context = {'user': user, 'manager': manager, 'formManager': formManager, 'formUser': formUser}
        return render(request, 'Poll/profile.html', context)


@login_required
def view_welcome(request):
    return render(request, 'Poll/welcome.html')


@login_required
def view_form_profile_bs(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ChangeProfileBSPoll(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ChangeProfileBSPoll(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-manager')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_personal_BS.html', context)


@login_required
def view_form_profile_bm(request):
    manager = BusinessManager.objects.get(userguiar__pk=request.user.pk)
    form = ChangeProfileBMPoll(instance=manager)
    context = {'manager': manager, 'form': form}
    if request.method == "POST":
        form = ChangeProfileBMPoll(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('poll-sales')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_personal_BM.html', context)


@login_required
def view_form_sales(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ChangeSaleFrom(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ChangeSaleFrom(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-quantity')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_sale.html', context)


@login_required
def view_form_quantity(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    dotaciones = Dotacion.objects.all()
    campos = []
    campos.clear()
    i = 1
    values = []
    values.clear()
    for dot in dotaciones:
        campo = DotacionEmpresarial.objects.get_or_create(user=user, dotacion=dot)
        campos.append([dot.title, campo[0].cantidad, i])
        values.append(campo[0].cantidad)
        i = i + 1
    formset = DotacionForm(n=i-1, values=values)
    if request.method == "POST":
        formset = DotacionForm(request.POST, n=i-1, values=values)
        if formset.is_valid():
            cantidad = []
            cantidad.clear()
            for j in range(i-1):
                cantidad.append(formset.cleaned_data['cantidad%d' % j])
            k = 0
            for dot in dotaciones:
                campo = DotacionEmpresarial.objects.get_or_create(user=user, dotacion=dot)
                campo[0].cantidad = cantidad[k]
                campo[0].save()
                k = k + 1
        print(formset.errors)
        return redirect('poll-process-list')
        #else:
         #   messages.error(request, "Error")
    context = {'user': user, 'campos': campos, 'formset': formset}
    return render(request, 'Poll/forms/form_dotacion.html', context)


@login_required
def view_form_process_list(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ProcessActivityForm(t="1")
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ProcessActivityForm(request.POST, t="1")
        if form.is_valid():
            dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            if not dependencias:
                for d in Dependencia.objects.all():
                    IntermediaDependenciaUser.objects.get_or_create(user=user, dependencia=d)
                dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            textos = []
            textos.clear()
            for campo in form.cleaned_data['nombre']:
                cambio = IntermediaDependenciaUser.objects.get(user=user, dependencia=campo.pk)
                cambio.selected = True
                cambio.save()
                textos.append(campo.nombre)
            for dep in dependencias:
                if dep.dependencia.tipo == "1":
                    if dep.dependencia.nombre not in textos:
                        dep.selected = False
                        dep.save()
            textos.clear()
            # return redirect('poll-transport')
            return redirect('poll-process')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_process_list.html', context)


@login_required
def view_process(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    grupo_preguntas = Pregunta.objects.filter(tipo=3)
    grupo_dependencias = IntermediaDependenciaUser.objects.filter(user=user)
    dependencias = []
    dependencias.clear()
    for dep in grupo_dependencias:
        if dep.dependencia.tipo == "1":
            if dep.selected:
                dependencias.append(dep.dependencia.nombre)
    preguntas = []
    preguntas.clear()
    for preg in grupo_preguntas:
        if preg.dependencia.nombre in dependencias:
            preguntas.append(preg)
    n = len(preguntas)
    form = PreguntaForm(n=n, p=preguntas)
    error = False
    context = {'user': user, 'form': form, 'errors': error, 'error_list': []}
    if request.method == "POST":
        form = PreguntaForm(request.POST, n=n, p=preguntas)
        if form.is_valid():
            # form = ActivityForm(request.POST, n=i-1, p=pre)
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            if not grupo_opciones:
                opciones = Opcion.objects.all()
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
                grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            else:
                for opcion in grupo_opciones:
                    if opcion.selected:
                        opcion.selected = False
                        opcion.save()
            for i in range(n):
                campo = 'opciones' + str(i)
                for o in form.cleaned_data[campo]:
                    if o not in grupo_opciones:
                        opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                        opcion.selected = True
                        opcion.save()
                        print(o)
                print("")
            print(form.errors)
            # return redirect('poll-control-risk')
            return redirect('poll-control')
        else:
            print("Hi")
            error = True
            context = {'user': user, 'form': form, 'errors': error, 'error_list': messages.error(request, "Error")}
            return render(request, 'Poll/forms/form_process.html', context)
            #   messages.error(request, "Error")
            # TODO: Generar correctamente mensajes de error en caso que se requiera
    #context = {'user': user, 'preg': preg, 'form': form}
    return render(request, 'Poll/forms/form_process.html', context)


@login_required
def view_transport_process(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    process = ProcessBusiness.objects.get(title="Transporte")
    if process not in user.process.all():
        user.transport.clear()
        return redirect('poll-manufacture')

    form = TransportProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = TransportProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-manufacture')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_transport.html', context)


@login_required
def view_manufacture_process(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    process = ProcessBusiness.objects.get(title="Manufactura")
    if process not in user.process.all():
        user.manufacture.clear()
        return redirect('poll-building')

    form = ManufactureProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ManufactureProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-building')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_manufacture.html', context)


@login_required
def view_building_process(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    process = ProcessBusiness.objects.get(title="Construcción")
    if process not in user.process.all():
        user.building.clear()
        return redirect('poll-services')

    form = BuildingProcessForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = BuildingProcessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-services')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_building.html', context)


@login_required
def view_services_process(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    process = ProcessBusiness.objects.get(title="Servicios Generales")
    if process not in user.process.all():
        user.general_services.clear()
        return redirect('poll-control-risk')

    form = GeneralServiceForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = GeneralServiceForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-control-risk')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_services.html', context)


@login_required
def view_control(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    preguntas = Pregunta.objects.filter(tipo=1)
    n = len(preguntas)
    form = PreguntaForm(n=n, p=preguntas)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = PreguntaForm(request.POST, n=n, p=preguntas)
        if form.is_valid():
            # form = ActivityForm(request.POST, n=i-1, p=pre)
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            if not grupo_opciones:
                opciones = Opcion.objects.all()
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
                grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            else:
                for opcion in grupo_opciones:
                    if opcion.selected:
                        opcion.selected = False
                        opcion.save()
            for i in range(n):
                campo = 'opciones' + str(i)
                for o in form.cleaned_data[campo]:
                    if o not in grupo_opciones:
                        opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                        opcion.selected = True
                        opcion.save()
                        print(o)
                print("")
            print(form.errors)
            return redirect('poll-activity-list')
        else:
            print("Hi")
            return render(request, 'Poll/forms/form_control.html', context)
            #   messages.error(request, "Error")
            # TODO: Generar correctamente mensajes de error en caso que se requiera
    #context = {'user': user, 'preg': preg, 'form': form}
    return render(request, 'Poll/forms/form_control.html', context)


@login_required
def view_control_risk(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ControlRiskForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ControlRiskForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-prevent-risk')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_risk.html', context)


@login_required
def view_prevent_risk(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = PreventRiskForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = PreventRiskForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # return redirect('poll-confirmed-explosive')
            return redirect('poll-activity-list')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_prevnet_risk.html', context)


@login_required
def view_form_activity_list(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ProcessActivityForm(t="2")
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ProcessActivityForm(request.POST, t="2")
        if form.is_valid():
            dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            if not dependencias:
                for d in Dependencia.objects.all():
                    IntermediaDependenciaUser.objects.get_or_create(user=user, dependencia=d)
                dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            textos = []
            textos.clear()
            for campo in form.cleaned_data['nombre']:
                cambio = IntermediaDependenciaUser.objects.get(user=user, dependencia=campo.pk)
                cambio.selected = True
                cambio.save()
                textos.append(campo.nombre)
            for dep in dependencias:
                if dep.dependencia.tipo == "2":
                    if dep.dependencia.nombre not in textos:
                        dep.selected = False
                        dep.save()
            textos.clear()
            # return redirect('poll-transport')
            return redirect('poll-activity')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_activity_list.html', context)


@login_required
def view_activity(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    grupo_preguntas = Pregunta.objects.filter(tipo=2)
    grupo_dependencias = IntermediaDependenciaUser.objects.filter(user=user)
    dependencias = []
    dependencias.clear()
    for dep in grupo_dependencias:
        if dep.dependencia.tipo == "2":
            if dep.selected:
                dependencias.append(dep.dependencia.nombre)
    preguntas = []
    preguntas.clear()
    for preg in grupo_preguntas:
        if preg.dependencia.nombre in dependencias:
            preguntas.append(preg)
    n = len(preguntas)
    form = PreguntaForm(n=n, p=preguntas)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = PreguntaForm(request.POST, n=n, p=preguntas)
        if form.is_valid():
            # form = ActivityForm(request.POST, n=i-1, p=pre)
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            if not grupo_opciones:
                opciones = Opcion.objects.all()
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
                grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            else:
                for opcion in grupo_opciones:
                    if opcion.selected:
                        opcion.selected = False
                        opcion.save()
            # print(grupo_opciones)
            print("")
            for i in range(n):
                campo = 'opciones' + str(i)
                print(form.cleaned_data[campo])
                for o in form.cleaned_data[campo]:
                    print(o)
                print("")
            for i in range(n):
                campo = 'opciones' + str(i)
                for o in form.cleaned_data[campo]:
                    if o not in grupo_opciones:
                        print(o)
                        opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                        opcion.selected = True
                        opcion.save()
                        print("")
                print("")
            print(form.errors)
            # return redirect('poll-control-risk')
            return redirect('poll-results')
        else:
            print("Hi")
            return render(request, 'Poll/forms/form_activity.html', context)
            #   messages.error(request, "Error")
            # TODO: Generar correctamente mensajes de error en caso que se requiera
    #context = {'user': user, 'preg': preg, 'form': form}
    return render(request, 'Poll/forms/form_activity.html', context)


@login_required
def view_confirmed_control_explosive(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ExplosiveConfirmedForm(instance=user)
    if request.method == "POST":
        form = ExplosiveConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.explosive_confirmed.option_explosive == "Sí":
                return redirect('poll-explosive')
            else:
                user.explosive_control.clear()
                return redirect('poll-confirmed-electricity')
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_explosive.html', context)


@login_required
def view_control_explosive(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ExplosiveControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ExplosiveControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-electricity')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_explosives.html', context)


@login_required
def view_confirmed_control_electricity(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ElectricityConfirmedForm(instance=user)
    if request.method == "POST":
        form = ElectricityConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.electricity_confirmed.option_electricity == "Sí":
                return redirect('poll-electricity')
            else:
                user.electricity_control.clear()
                return redirect('poll-confirmed-substance')
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_electricity.html', context)


@login_required
def view_control_electricity(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ElectricityControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ElectricityControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-substance')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_electricity.html', context)


@login_required
def view_confirmed_substances(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = SubstancesConfirmedForm(instance=user)
    if request.method == "POST":
        form = SubstancesConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.substance_confirmed.option_substance == "Sí":
                return redirect('poll-substance')
            else:
                user.substance_control.clear()
                return redirect('poll-confirmed-height')
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_substance.html', context)


@login_required
def view_control_substances(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = SubstanceControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = SubstanceControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-confirmed-height')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_substance.html', context)


@login_required
def view_confirmed_height(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = HeightConfirmedForm(instance=user)
    if request.method == "POST":
        form = HeightConfirmedForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.height_confirmed.option_height == "Sí":
                return redirect('poll-height')
            else:
                user.height_control.clear()
                return redirect('poll-results')
    context = {'form': form}
    return render(request, 'Poll/forms/form_confirm_height.html', context)


@login_required
def view_control_height(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = HeightControlForm(instance=user)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = HeightControlForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-results')
        else:
            messages.error(request, "Error")
    return render(request, 'Poll/forms/form_control_height.html', context)


class UpdateManagerView(UpdateView):
    model = BusinessManager
    form_class = ChangeProfileBMPoll
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(UpdateManagerView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(UpdateManagerView, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            user = UserGuiar.objects.get(pk=self.request.user.pk)
            user.email_manager = form.cleaned_data['email']
            user.save()
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = BusinessManager.objects.get(userguiar__rut=self.request.user)
        return obj


class UpdateUserView(UpdateView):
    model = UserGuiar
    form_class = ChangeProfileBSPoll
    success_url = '/form-success/'

    def form_invalid(self, form):
        response = super(UpdateUserView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(UpdateUserView, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            data = {
                'messages': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response

    def get_object(self, queryset=None):
        obj = UserGuiar.objects.get(rut=self.request.user)
        return obj


@login_required
def view_results(request):
    pk = request.user.pk
    # [Nombre de la poliza, maximo puntaje, puntaje obtenido, id de la Poliza]
    desgloce = []
    desgloce.clear()
    # Resultado global independiente de las polizas
    total = 0
    # Maximo y Minimo valor obtenible en la encuesta (para ajustar la representacion grafica)
    maximo = 0
    minimo = 0
    # Se generan las categorias a considerar en los resultados
    polizas = SubPoliza.objects.all()
    for pol in polizas:
        desgloce.append([pol.name, 0, 0, pol.id, pol.categoria.name])
    # Este codigo no funcionara si una poliza es eliminada, en tal caso habria que buscar entre las polizas la que
    # coincida con opcion.poliza.pk obteniendo su posicion y utilizando este valor en vez de la referencia directa
    # En esta parte si "Responsabilidad Civil de Empresa" no es la primera poliza en la tabla, entonces esto dejara de
    # funcionar, en tal caso habria que buscar el indice en el que se encuentra esta poliza o su equivalente

    # Se obtienen los maximos de cada poliza revisando cada opcion de cada pregunta
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
    user = UserGuiar.objects.get(pk=pk)

    dotaciones = Dotacion.objects.all()
    for dotacion in dotaciones:
        campo = DotacionEmpresarial.objects.get_or_create(user=user, dotacion=dotacion)
        cantidad = campo[0].cantidad

    # dotaciones = DotacionEmpresarial.objects.get(user=user)
        rangos = RangosDotacion.objects.filter(dotacion=dotacion)
        for rango in rangos:
            pos = rango.poliza.pk - 1
            if rango.min_value > rango.max_value:
                if cantidad >= rango.min_value:  # caso valor en el ultimo rango
                    # Se agrega el resultado correspondiente al riesgo de la poliza vinculada
                    if pos != 0:
                        desgloce[pos][2] += rango.ri_value * rango.min_value
                    desgloce[0][2] += rango.ri_value * rango.min_value
                    total += rango.ri_value * rango.min_value
                # Se agrega el maximo correspondiente independiente si se encuentra o no dentro del rango asociado
                if pos != 0:
                    desgloce[pos][1] += rango.ri_value * rango.min_value
                desgloce[0][1] += rango.ri_value * rango.min_value
                maximo += rango.ri_value * rango.min_value
            elif cantidad >= rango.min_value:
                if cantidad < rango.max_value:  # caso valor dentro del rango
                    # Se agrega el resultado correspondiente al riesgo de la poliza vinculada
                    if pos != 0:
                        desgloce[pos][2] += rango.ri_value * cantidad
                    desgloce[0][2] += rango.ri_value * cantidad
                    total += rango.ri_value * cantidad

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
    manejo_riesgo = 0
    if user.risk_management:
        manejo_riesgo = user.risk_management.ri_risk
    # Se lleva la cuenta de los resultados de Prevencionista de Riesgo
    prevencionista = 0
    if user.risk_prevent:
        prevencionista = user.risk_prevent.ri_prevent

    # Se obtiene el total de amortiguacion de riesgo en %, aqui no hay un valor maximo que aumente el riesgo
    amortiguacion = (manejo_riesgo + prevencionista)/100

    # Se lleva la cuenta de los resultados de Explosivos
    if user.explosive_confirmed:
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
    if user.electricity_confirmed:
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
    if user.substance_confirmed:
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
    if user.height_confirmed:
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

    is_empty = 0
    for d in desgloce:
        if d[2] != 0:
            is_empty = 1
        d[2] = d[2] * (1 - amortiguacion)
    total = total * (1 - amortiguacion)
    if is_empty == 0:
        return redirect('home')
    else:
        for d in desgloce:
            print(d[0], d[1], d[2], d[3])

        desgloce_ordenado = []
        desgloce_ordenado.clear()
        for des in desgloce:
            # Se filtran los resultados nulos
            if des[2] != 0:
                # Este nuevo arreglo tiene [Nombre Poliza, Maximo Poliza, Resultado Poliza, ID Poliza]
                desgloce_ordenado.append([des[0], des[1], round((des[2]/des[1])*100, 2), des[3]])

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
            "customer_name": "Name",
            "amount": 1,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Reporte.pdf"
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content

            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return
