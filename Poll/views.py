from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import *

from Poll.forms import *
from Poll.models import *
from Home.models import UserGuiar, BusinessManager, Dotacion, DotacionEmpresarial, RangosDotacion, IntermediaUserOpcion
# PDF
from django.views.generic import View
from .utils import render_to_pdf
# from django.template.loader import get_template


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
            # print(username)
            username = username.replace(".", "")
            # print(username)
            if username[-2] != "-":
                # print("sin guion")
                num = username[:-1]
                div = username[-1:]
                username = str(num) + "-" + str(div)
            # print(username)
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
        form_manager = ChangeProfileBMPoll(instance=manager)
        form_user = ChangeProfileBSPoll(instance=user)
        context = {'user': user, 'manager': manager, 'formManager': form_manager, 'formUser': form_user}
        return render(request, 'Poll/profile.html', context)


@login_required
def view_welcome(request):
    return render(request, 'Poll/welcome.html')


@login_required
def view_form_profile_bs(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ChangeProfileBSPoll(instance=user)
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ChangeProfileBSPoll(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('poll-manager')
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return render(request, 'Poll/forms/form_personal_BS.html', context)


@login_required
def view_form_profile_bm(request):
    manager = BusinessManager.objects.get(userguiar__pk=request.user.pk)
    form = ChangeProfileBMPoll(instance=manager)
    context = {'manager': manager, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ChangeProfileBMPoll(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('poll-sales')
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return render(request, 'Poll/forms/form_personal_BM.html', context)


@login_required
def view_form_sales(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ChangeSaleFrom(instance=user)
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
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
    if request.is_ajax and request.method == "POST":
        formset = DotacionForm(request.POST, n=i-1, values=values)
        print(formset)
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
            return redirect('poll-process-list')
        else:
            messages.error(request, "Error")
    context = {'user': user, 'campos': campos, 'formset': formset}
    return render(request, 'Poll/forms/form_dotacion.html', context)


@login_required
def view_form_process_list(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ProcessListForm(t="1")
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ProcessListForm(request.POST, t="1")
        if form.is_valid():
            dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            grupo_dependencias = Dependencia.objects.all()
            if dependencias.count() != grupo_dependencias.count():
                for d in grupo_dependencias:
                    IntermediaDependenciaUser.objects.get_or_create(user=user, dependencia=d)
            else:
                for dep in dependencias:
                    if dep.dependencia.tipo == "1":
                        dep.selected = False
                        dep.save()
            for campo in form.cleaned_data['nombre']:
                cambio = IntermediaDependenciaUser.objects.get(user=user, dependencia=campo.pk)
                cambio.selected = True
                cambio.save()
            return JsonResponse({"url": "poll6"})
        else:
            return JsonResponse({"error": form.errors}, status=400)
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
    form = ProcessForm(n=n, p=preguntas)
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ProcessForm(request.POST, n=n, p=preguntas)
        dependencias.clear()
        preguntas.clear()
        if form.is_valid():
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            opciones = Opcion.objects.all()
            if grupo_opciones.count() != opciones.count():
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
            else:
                for opcion in grupo_opciones:
                    if opcion.opcion.pregunta.tipo.pk == 3:
                        opcion.selected = False
                        opcion.save()
            for i in range(n):
                campo = 'opciones' + str(i)
                for o in form.cleaned_data[campo]:
                    opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                    opcion.selected = True
                    opcion.save()
            return JsonResponse({"url": "poll7"})
        else:
            return JsonResponse({"error": formset.errors}, status=400)
    return render(request, 'Poll/forms/form_process.html', context)


@login_required
def view_control(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    preguntas = Pregunta.objects.filter(tipo=1)
    n = len(preguntas)
    form = ControlForm(n=n, p=preguntas)
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ControlForm(request.POST, n=n, p=preguntas)
        if form.is_valid():
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            opciones = Opcion.objects.all()
            if grupo_opciones.count() != opciones.count():
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
            else:
                for opcion in grupo_opciones:
                    if opcion.opcion.pregunta.tipo.pk == 1:
                        opcion.selected = False
                        opcion.save()
            for i in range(n):
                campo = 'opciones' + str(i)
                o = form.cleaned_data[campo]
                opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                opcion.selected = True
                opcion.save()
            return JsonResponse({"url": "poll8"})
        else:
            return JsonResponse({"error": formset.errors}, status=400)
    return render(request, 'Poll/forms/form_control.html', context)


@login_required
def view_form_activity_list(request):
    user = UserGuiar.objects.get(pk=request.user.pk)
    form = ActivityListForm(t="2")
    context = {'user': user, 'form': form}
    if request.is_ajax and request.method == "POST":
        form = ActivityListForm(request.POST, t="2")
        if form.is_valid():
            dependencias = IntermediaDependenciaUser.objects.filter(user=user)
            grupo_dependencias = Dependencia.objects.all()
            if dependencias.count() != grupo_dependencias.count():
                for d in grupo_dependencias:
                    IntermediaDependenciaUser.objects.get_or_create(user=user, dependencia=d)
            else:
                for dep in dependencias:
                    if dep.dependencia.tipo == "2":
                        dep.selected = False
                        dep.save()
            i = 0
            for campo in form.cleaned_data['nombre']:
                cambio = IntermediaDependenciaUser.objects.get(user=user, dependencia=campo.pk)
                cambio.selected = True
                cambio.save()
                i += 1
            if i == 0:
                return JsonResponse({"url": "poll-results"})
            else:
                return JsonResponse({"url": "poll9"})
        else:
            return JsonResponse({"error": formset.errors}, status=400)
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
    form = ActivityForm(n=n, p=preguntas)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        form = ActivityForm(request.POST, n=n, p=preguntas)
        if form.is_valid():
            grupo_opciones = IntermediaUserOpcion.objects.filter(user=user)
            opciones = Opcion.objects.all()
            if grupo_opciones.count() != opciones.count():
                for op in opciones:
                    IntermediaUserOpcion.objects.get_or_create(user=user, opcion=op)
            else:
                for opcion in grupo_opciones:
                    if opcion.opcion.pregunta.tipo.pk == 2:
                        opcion.selected = False
                        opcion.save()
            for i in range(n):
                campo = 'opciones' + str(i)
                for o in form.cleaned_data[campo]:
                    opcion = IntermediaUserOpcion.objects.get(user=user, opcion=o)
                    opcion.selected = True
                    opcion.save()
            return JsonResponse({"url": "poll-results"})
        else:
            return JsonResponse({"error": formset.errors}, status=400)
    return render(request, 'Poll/forms/form_activity.html', context)


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
        print(response)
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


def buscar_indice(n, lista):
    for i in range(len(lista)):
        if n == lista[i][3]:
            return i
    return -1


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
        desgloce.append([pol.name, 0, 0, pol.pk, pol.categoria.name])

    # Se obtiene el usuario del cual se lee la informacion
    user = UserGuiar.objects.get(pk=pk)

    dotaciones = Dotacion.objects.all()
    for dotacion in dotaciones:
        campo = DotacionEmpresarial.objects.get_or_create(user=user, dotacion=dotacion)
        cantidad = campo[0].cantidad

    # dotaciones = DotacionEmpresarial.objects.get(user=user)
        rangos = RangosDotacion.objects.filter(dotacion=dotacion)
        for rango in rangos:
            pos = buscar_indice(rango.poliza.pk - 1, desgloce)
            if rango.min_value > rango.max_value:
                if cantidad >= rango.min_value:  # caso valor en el ultimo rango
                    # Se agrega el resultado correspondiente al riesgo de la poliza vinculada
                    desgloce[pos][2] += rango.ri_value * rango.min_value
                    total += rango.ri_value * rango.min_value
                # Se agrega el maximo correspondiente independiente si se encuentra o no dentro del rango asociado
                desgloce[pos][1] += rango.ri_value * rango.min_value
                maximo += rango.ri_value * rango.min_value
            elif cantidad >= rango.min_value:
                if cantidad < rango.max_value:  # caso valor dentro del rango
                    # Se agrega el resultado correspondiente al riesgo de la poliza vinculada
                    desgloce[pos][2] += rango.ri_value * cantidad
                    total += rango.ri_value * cantidad

    # Se obtiene el listado de todas las dependencias marcadas y se procesan
    dependencia = IntermediaDependenciaUser.objects.filter(user=user)
    for dep in dependencia:
        risk = dep.dependencia.riesgo
        if dep.dependencia.tipo == "1":
            if dep.selected:
                preguntas = Pregunta.objects.filter(dependencia=dep.dependencia)
                for pregunta in preguntas:
                    if pregunta.tipo.pk == 3:
                        opciones = Opcion.objects.filter(pregunta=pregunta)
                        for opcion in opciones:
                            maximo += opcion.riesgo * risk
                            opc = IntermediaUserOpcion.objects.filter(user=user, opcion=opcion)
                            if opc[0].selected:
                                total += opc[0].opcion.riesgo * risk
                            opcion_poliza = PolizaOpcion.objects.filter(opcion=opc[0].opcion)
                            for op in opcion_poliza:
                                index = buscar_indice(op.poliza.pk, desgloce)
                                if opc[0].selected:
                                    desgloce[index][2] += op.opcion.riesgo * risk
                                if op.opcion.riesgo >= 0:
                                    desgloce[index][1] += op.opcion.riesgo * risk
        if dep.dependencia.tipo == "2":
            if dep.selected:
                total = float(total) + float(risk)
            maximo += risk
            preguntas = Pregunta.objects.filter(dependencia=dep.dependencia)
            riesgo_total = 0
            riesgo = 0
            for pregunta in preguntas:
                opciones = IntermediaUserOpcion.objects.filter(user=user)
                for opcion in opciones:
                    if opcion.opcion.pregunta == pregunta:
                        riesgo_total += opcion.opcion.riesgo
                        if opcion.selected:
                            riesgo += opcion.opcion.riesgo
            riesgo_parcial = float(riesgo / riesgo_total)
            riesgo_agregado = (float(risk) * 0.8) * riesgo_parcial
            total = float(total) + float(riesgo_agregado)
    opciones = IntermediaUserOpcion.objects.filter(user=user)
    amortiguacion = 0
    for o in opciones:
        if o.opcion.pregunta.tipo.pk == 1:
            print(o.opcion.texto)
            if o.selected:
                if o.opcion.texto == "Empresa cuenta con Sistem Integrado de Gestion" or \
                        o.opcion.texto == "Gerencia / Administración de Riesgos (ISO 31.000:2009)":
                    amortiguacion = o.opcion.riesgo
                else:
                    amortiguacion += o.opcion.riesgo

    ventas = user.sales.amortiguador
    # Evitar problemas de rebalse del amortiguador
    if amortiguacion > 45:
        amortiguacion = 45
    amortiguacion += ventas
    is_empty = 0
    for d in desgloce:
        if d[2] != 0:
            is_empty = 1
        print(d[0], d[1], d[2], d[3])
        d[2] = d[2] * (1 - (amortiguacion/100))
    print("")
    print("Total: ", total)
    print("Amortiguacion: ", amortiguacion)
    total = total * float(1 - (amortiguacion/100))

    if total > maximo:
        total = maximo

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
        print("Total: ", total)
        res_por = total / float(maximo)
        res_img = (379 + 19) * res_por
        res_fin = (379 + 19) - res_img
        res_fin = int(res_fin)
        cuartil = maximo / 4
        print("este es el maximo", maximo)

        if total < cuartil:
            color = "VERDE"
        elif cuartil <= total < (2 * cuartil):
            color = "AMARILLO"
        elif (2 * cuartil) <= total <= (3 * cuartil):
            color = "ANARANJADO"
        else:
            color = "ROJO"
        print(desgloce_ordenado)
        return render(request, 'Poll/results.html',
                      {'maximo': maximo, 'minimo': minimo, 'total': total, 'res_fin': res_fin,
                       'color': color, 'desgloce': desgloce_ordenado})


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        polizas = request.GET.getlist('polizas[]')
        user = UserGuiar.objects.get(pk=self.request.user.pk)
        dotacion = DotacionEmpresarial.objects.get(user_id=user.id, dotacion_id=1)
        vehiculos_ligeros = DotacionEmpresarial.objects.get(user_id=user.id, dotacion_id=3)
        vehiculos_pesados = DotacionEmpresarial.objects.get(user_id=user.id, dotacion_id=5)
        context = {
            "nombre_empresa": user.name,
            "monto_recomendado": 0,
            "monto_asegurado": 0,
            "vehiculos_ligeros": 0,
            "vehiculos_pesados": 0,
            "accidentes": 0,
            "equipos": 0,
            "eco_motor": 0,
            "transporte_acido": 0
        }
        if user.sales_id == 1 and dotacion.cantidad < 200:
            context['monto_recomendado'] = 1000
            context['monto_asegurado'] = 500
        elif user.sales_id == 2 and dotacion.cantidad < 200:
            context['monto_recomendado'] = 2000
            context['monto_asegurado'] = 1000
        elif user.sales_id == 3 and dotacion.cantidad < 200:
            context['monto_recomendado'] = 3000
            context['monto_asegurado'] = 1000
        elif user.sales_id == 4 and dotacion.cantidad < 200:
            if dotacion.cantidad >= 50:
                context['monto_recomendado'] = 7500
                context['monto_asegurado'] = 2500
            else:
                context['monto_recomendado'] = 5000
                context['monto_asegurado'] = 1500
        elif user.sales_id == 4 and dotacion.cantidad >= 200:
            context['monto_recomendado'] = 10000
            context['monto_asegurado'] = 2500
        if vehiculos_ligeros.cantidad > 0:
            context['vehiculos_ligeros'] = 1
        if vehiculos_pesados.cantidad > 0:
            context['vehiculos_pesados'] = 1
        if "1" in polizas:
            context['accidentes'] = 1
        if "7" in polizas:
            context['equipos'] = 1
        if "8" in polizas:
            context['eco_motor'] = 1
        if "9" in polizas:
            context['transporte_acido'] = 1
        # template = get_template('invoice.html')
        # html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        print(context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Reporte.pdf"
            content = "inline; filename='%s'" % filename
            response['Content-Disposition'] = content

            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return
