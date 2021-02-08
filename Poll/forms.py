from django import forms
from reportlab import xrange

from Home.models import UserGuiar, City, Town, BusinessManager, Dotacion, DotacionEmpresarial
from Poll.models import Sales, Opcion, Pregunta, Dependencia


class LoginForm(forms.Form):
    rut = forms.CharField(label="", widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'class': 'input',
        'placeholder': 'rut'
    }))

    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'password'
    }))


class ChangeProfileBSPoll(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['name', 'rut', 'seniority', 'address', 'city', 'town']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'rut': forms.TextInput(attrs={'class': 'input', 'readonly':'readonly'}),
            'seniority': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.TextInput(attrs={'class': 'input'}),
        }


class ChangeProfileBMPoll(forms.ModelForm):
    class Meta:
        model = BusinessManager
        fields = "__all__"

        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'input'}),
            'rut_bm': forms.TextInput(attrs={'class': 'input', 'readonly':'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.NumberInput(attrs={'class': 'input'})
        }


class ChangeSaleFrom(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['sales']

        widgets = {
            'sales': forms.RadioSelect
        }


class DotacionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        values = kwargs.pop('values', list)
        super(DotacionForm, self).__init__(*args, **kwargs)
        for i in xrange(n):
            self.fields['cantidad%d' % i] = forms.IntegerField(min_value=0, initial=values[i])
            self.fields['cantidad%d' % i].widget.attrs.update({'class': 'input'})


class ProcessListForm(forms.Form):# Seleccionar procesos involucrados

    def __init__(self, *args, **kwargs):
        t = kwargs.pop('t', int)
        super(ProcessListForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.filter(tipo=t),
                                                               widget=forms.CheckboxSelectMultiple)


class ActivityListForm(forms.Form):# Seleccionar actividades involucradas

    def __init__(self, *args, **kwargs):
        t = kwargs.pop('t', int)
        super(ActivityListForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.filter(tipo=t),
                                                               widget=forms.CheckboxSelectMultiple, required=False)


class ProcessForm(forms.Form):# Seleccionar opcion en Procesos
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        p = kwargs.pop('p', list)
        super(ProcessForm, self).__init__(*args, **kwargs)
        for i in range(n):
            self.fields['titulo%d' % i] = forms.CharField(
                initial=p[i].texto, required=False,
                widget=forms.HiddenInput(attrs={'readonly': 'readonly'})
            )
            self.fields['opciones%d' % i] = forms.ModelMultipleChoiceField(
                queryset=Opcion.objects.filter(pregunta=p[i]), required=True,
                widget=forms.CheckboxSelectMultiple,
            )


class ControlForm(forms.Form):# Seleccionar opcion en control de riesgo
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        p = kwargs.pop('p', list)
        super(ControlForm, self).__init__(*args, **kwargs)
        for i in range(n):
            self.fields['titulo%d' % i] = forms.CharField(
                initial=p[i].texto, required=False,
                widget=forms.HiddenInput(attrs={'readonly': 'readonly'})
            )
            self.fields['opciones%d' % i] = forms.ModelChoiceField(
                queryset=Opcion.objects.filter(pregunta=p[i]),
                widget=forms.RadioSelect,
            )


class ActivityForm(forms.Form):# Seleccionar opcion en Actividades
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        p = kwargs.pop('p', list)
        super(ActivityForm, self).__init__(*args, **kwargs)
        for i in range(n):
            self.fields['titulo%d' % i] = forms.CharField(
                initial=p[i].texto, required=True, disabled=True,
                widget=forms.HiddenInput(attrs={'readonly': 'readonly'})
            )
            self.fields['opciones%d' % i] = forms.ModelMultipleChoiceField(
                queryset=Opcion.objects.filter(pregunta=p[i]), required=False,
                widget=forms.CheckboxSelectMultiple,
            )
