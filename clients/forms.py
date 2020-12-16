from datetime import date

from django import forms

from clients.models import Client, Order
from menus.models import Option, Menu


class ClientForm(forms.ModelForm):
    """Defines Client form"""
    name = forms.CharField(label='Name')
    phone_number = forms.CharField(label='Phone number')

    class Meta:
        model = Client
        fields = '__all__'


class OrderForm(forms.ModelForm):
    """Defines Order form"""
    today = date.today()
    menu = Menu.objects.filter(date=today)  # Retrieves menu of the day info

    option = forms.ModelChoiceField(queryset=Option.objects.filter(menu__in=menu),
                                    initial=0)
    comments = forms.CharField(label='Special requests',
                               widget=forms.TextInput(attrs={'style': 'padding-right: 20rem;'}), empty_value='None',
                               required=False)

    class Meta:
        model = Order
        fields = ('option', 'comments',)