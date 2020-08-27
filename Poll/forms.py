from django import forms

from Home.models import UserGuiar, City, Town, BusinessManager


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


class ChangeProfileBSPoll(forms.Form):
    name_BS = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    rut_BS = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    seniority = forms.IntegerField(min_value=0, max_value=10000, widget=forms.NumberInput(attrs={
        'class': 'input'
    }))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    city = forms.ModelChoiceField(queryset=City.objects.all())
    # town = forms.ModelMultipleChoiceField(queryset=City.objects.none(),
                                          # widget=forms.Select())



"""
    def __init__(self, city_q, *args, **kwargs):
        super(ChangeProfileBSPoll, self).__init__(*args, **kwargs)
        # self.fields['town'].queryset = Town.objects.filter(city__name_city=city_q)
"""


class ChangeProfileBMPoll(forms.Form):
    rut_bm = forms.CharField(max_length=12)
    fullname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.IntegerField()
