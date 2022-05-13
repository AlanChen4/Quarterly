from django import forms
from django.forms import formset_factory


class PortfolioForm(forms.Form):
    nickname = forms.CharField(max_length=255)
    risk_tolerance = forms.ChoiceField(choices=(
        ('Conservative', 'Conservative'),
        ('Moderate', 'Moderate'),
        ('Aggressive', 'Aggressive'),
    ))
    description = forms.CharField(label='Additional information', help_text="Context such as your age, goals, risk tolerance, or why you picked certain assets are helpful, but not necessary", widget=forms.Textarea, required=False)


class AssetForm(forms.Form):
    ticker = forms.CharField(max_length=8)
    name = forms.CharField(max_length=255)
    holdings = forms.FloatField(label='Amount ($)')

AssetFormSet = formset_factory(AssetForm)
