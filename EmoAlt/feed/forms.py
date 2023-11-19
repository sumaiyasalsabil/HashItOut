from django import forms

class StartButtonForm(forms.Form):
    
    clicked = forms.BooleanField()

