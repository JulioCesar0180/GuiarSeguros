from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserGuiar, BusinessManager


class UserGuiarCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserGuiar
        fields = ('rut',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CreateManagerForm(forms.ModelForm):
    class Meta:
        model = BusinessManager
        fields = ['fullname', 'rut_bm', 'email', 'phone']

        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'Nombre Completo',
                                               'autocomplete': 'off'}),
            'rut_bm': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'Rut',
                                             'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'input gs-input', 'placeholder': 'Email',
                                             'autocomplete': 'off'}),
            'phone': forms.NumberInput(attrs={'class': 'input gs-input', 'placeholder': 'Celular',
                                              'autocomplete': 'off'})
        }


class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input gs-input', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input gs-input', 'placeholder': 'Confirmar Contraseña'}))

    class Meta:
        model = UserGuiar
        fields = ['rut', 'name', 'city', 'town', 'address', 'seniority', 'password1', 'password2']

        widgets = {
            'rut': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'RUT', 'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'Razón Social', 'autocomplete': 'off'}),
            'seniority': forms.NumberInput(attrs={'class': 'input gs-input', 'placeholder': 'Antigüedad de la empresa', 'autocomplete': 'off'}),
            'address': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'Dirección', 'autocomplete': 'off'}),
            'town': forms.TextInput(attrs={'class': 'input gs-input', 'placeholder': 'Comuna', 'autocomplete': 'off'}),
        }
