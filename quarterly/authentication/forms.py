from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = CustomUser
        fields = ('email', 'display_name', 'visible')
