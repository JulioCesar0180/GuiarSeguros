from django import forms

from Home.models import UserGuiar, City, Town, BusinessManager
from Poll.models import Sales


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
            'town': forms.TextInput(attrs={'class': 'input'})
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


class QuantityEmpForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['n_emp_hired', 'n_cont_emp', 'n_veh_com_light',
                  'n_veh_com_cont', 'n_veh_com_heavy', 'n_veh_com_heavy_cont',
                  'n_mach_heavy', 'n_mach_heavy_cont']

        widgets = {
            'n_emp_hired': forms.NumberInput(attrs={'class': 'input'}),
            'n_cont_emp': forms.NumberInput(attrs={'class': 'input'}),
            'n_veh_com_light': forms.NumberInput(attrs={'class': 'input'}),
            'n_veh_com_cont': forms.NumberInput(attrs={'class': 'input'}),
            'n_veh_com_heavy': forms.NumberInput(attrs={'class': 'input'}),
            'n_veh_com_heavy_cont': forms.NumberInput(attrs={'class': 'input'}),
            'n_mach_heavy': forms.NumberInput(attrs={'class': 'input'}),
            'n_mach_heavy_cont': forms.NumberInput(attrs={'class': 'input'})
        }


class ProcessForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['process']

        widgets = {
            'process': forms.CheckboxSelectMultiple
        }


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
            'risk_management': forms.CheckboxSelectMultiple
        }


class PreventRiskForm(forms.ModelForm):
    class Meta:
        model = UserGuiar
        fields = ['risk_prevent']

        widgets = {
            'risk_prevent': forms.CheckboxSelectMultiple
        }


class ConfirmedForm(forms.Form):
    CHOICE = [(True, "Sí"),
              (False, "No")]
    confirm = forms.ChoiceField(choices=CHOICE, widget=forms.RadioSelect)
