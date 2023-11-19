from django import forms
from django.forms.widgets import HiddenInput

class StartButtonForm(forms.Form):
    
    clicked = forms.BooleanField(widget=HiddenInput())

