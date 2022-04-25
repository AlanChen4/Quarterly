from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'dob', )
        labels = {
            'dob': 'Date of Birth'
        }
        widgets = {
            'dob': DateInput()
        }

