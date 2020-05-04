from django import forms

class SearchForm(forms.Form):
    product_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}),
        required=True
    )