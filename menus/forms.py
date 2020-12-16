from django import forms
from .models import *


class MenuForm(forms.ModelForm):
    """Defines Menu form"""
    date = forms.DateField(label='Date: ', widget=forms.DateInput(attrs={'id': 'date-input',
                                                                         'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Menu
        fields = '__all__'


class OptionForm(forms.ModelForm):
    """Defines Option form"""
    content = forms.CharField(label='Add a menu option here',
                              widget=forms.TextInput(attrs={'style': 'padding-right: 20rem;'}))

    class Meta:
        model = Option
        fields = ('content',)
