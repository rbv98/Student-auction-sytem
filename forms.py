from django import forms
from .models import Users

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ['type']
        fields = ['name', 'email', 'password']  # Include only the necessary fields
        widgets = {
            'password': forms.PasswordInput(),  # Use a password input widget for the password field
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
