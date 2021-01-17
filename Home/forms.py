from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django import forms

from .models import UserGuiar, BusinessManager, City, Town


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

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Seleccione una Ciudad",
        widget=forms.Select(attrs={'class': 'input gs-input'}))

    town = forms.ModelChoiceField(
        queryset=Town.objects.all(),
        empty_label="Seleccione una Comuna",
        widget=forms.Select(attrs={'class': 'input gs-input'})
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input gs-input', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input gs-input', 'placeholder': 'Confirmar Contraseña'})


class CreateRecuperarForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'email'
        })
    )

class TokenForm(forms.Form):
    token = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input'
        }),
        required = True
    )

class NewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        }),
        strip=False,
    )

class PasswordResetFormGS(PasswordResetForm):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'email'
        })
    )


class SetPasswordFormGS(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        }),
        strip=False,
    )


class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input'
            }
        )
    )

    new_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input'
            }
        )
    )

    confirm_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input'
            }
        )
    )