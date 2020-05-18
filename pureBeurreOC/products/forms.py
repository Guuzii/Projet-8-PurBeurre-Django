from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

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
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom', 'required': 'true'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'true'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe', 'type': 'password'})
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'username': "Un utilisateur avec cet identifiant existe déjà",
            }
        }

    # def validate_email_doesnt_exists(email):
    #     if User.objects.filter(email__iexact=email).exists(): # check if email exists
    #         raise ValidationError("Un utilisateur avec l'email %(email)s existe déjà.", code='email', params={'email': email})
        
    
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
