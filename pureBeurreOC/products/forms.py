from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    product_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}),
        required=True
    )

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Identifiant'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe', 'type': 'password'})
        }
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Identifiant'}),
        required=True
    )

    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        required=True
    )
