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
            'rut': forms.TextInput(attrs={'class': 'input'}),
            'seniority': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.TextInput(attrs={'class': 'input'}),
        }


"""
    def __init__(self, city_q, *args, **kwargs):
        super(ChangeProfileBSPoll, self).__init__(*args, **kwargs)
        # self.fields['town'].queryset = Town.objects.filter(city__name_city=city_q)
"""


class ChangeProfileBMPoll(forms.ModelForm):
    class Meta:
        model = BusinessManager
        fields = "__all__"

        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'input'}),
            'rut_bm': forms.TextInput(attrs={'class': 'input'}),
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
            

class ProcessForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['process']

        widgets = {
            'process': forms.CheckboxSelectMultiple
        }


class ProcessActivityForm(forms.Form):

    def __init__(self, *args, **kwargs):
        t = kwargs.pop('t', int)
        super(ProcessActivityForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ModelMultipleChoiceField(queryset=Dependencia.objects.filter(tipo=t),
                                                               widget=forms.CheckboxSelectMultiple)


class ActivityForm(forms.Form):

    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        p = kwargs.pop('p', object)
        super(ActivityForm, self).__init__(*args, **kwargs)
        for i in xrange(n):
            self.fields['opcion%d' % i] = forms.ModelMultipleChoiceField(queryset=Opcion.objects.filter(pregunta=p[i]))


class PreguntaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n', int)
        p = kwargs.pop('p', list)
        super(PreguntaForm, self).__init__(*args, **kwargs)
        for i in range(n):
            self.fields['titulo%d' % i] = forms.CharField(
                initial=p[i].texto, required=False,
                widget=forms.HiddenInput(attrs={'readonly': 'readonly'})
            )
            self.fields['opciones%d' % i] = forms.ModelMultipleChoiceField(
                queryset=Opcion.objects.filter(pregunta=p[i]), required=True,
                widget=forms.CheckboxSelectMultiple,
            )


class TransportProcessForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['transport']

        widgets = {
            'transport': forms.CheckboxSelectMultiple
        }


class ManufactureProcessForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['manufacture']

        widgets = {
            'manufacture': forms.CheckboxSelectMultiple
        }


class BuildingProcessForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['building']

        widgets = {
            'building': forms.CheckboxSelectMultiple
        }


class GeneralServiceForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['general_services']

        widgets = {
            'general_services': forms.CheckboxSelectMultiple
        }


class ControlRiskForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['risk_management']

        widgets = {
            'risk_management': forms.RadioSelect
        }


class PreventRiskForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['risk_prevent']

        widgets = {
            'risk_prevent': forms.RadioSelect
        }


class ConfirmedControlForm(forms.Form):
    CHOICE = [(True, "Sí"),
              (False, "No")]
    confirm = forms.ChoiceField(choices=CHOICE, widget=forms.RadioSelect)


class ExplosiveControlForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['explosive_control']

        widgets = {
            'explosive_control': forms.CheckboxSelectMultiple
        }


class ElectricityControlForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['electricity_control']

        widgets = {
            'electricity_control': forms.CheckboxSelectMultiple
        }


class SubstanceControlForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['substance_control']

        widgets = {
            'substance_control': forms.CheckboxSelectMultiple
        }


class HeightControlForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['height_control']

        widgets = {
            'height_control': forms.CheckboxSelectMultiple
        }


class ExplosiveConfirmedForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['explosive_confirmed']

        widgets = {
            'explosive_confirmed': forms.RadioSelect
        }


class ElectricityConfirmedForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['electricity_confirmed']

        widgets = {
            'electricity_confirmed': forms.RadioSelect
        }


class SubstancesConfirmedForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['substance_confirmed']

        widgets = {
            'substance_confirmed': forms.RadioSelect
        }


class HeightConfirmedForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['height_confirmed']

        widgets = {
            'height_confirmed': forms.RadioSelect
        }
