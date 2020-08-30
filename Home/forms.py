from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserGuiar, BusinessManager


class UserGuiarCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserGuiar
        fields = ('username',)

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
            'fullname': forms.TextInput(attrs={'class': 'input'}),
            'rut_bm': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.NumberInput(attrs={'class': 'input'})
        }
