from django.forms import ModelForm , TextInput
from django import forms
from .models import ShippingAddress

class Shipping_address(ModelForm):

    class Meta:
        model = ShippingAddress
        exclude = ['user']
        widgets = {
            'address':TextInput(attrs={'class':'form-control','placeholder':'34 Main St'}),
            'apartment_address':TextInput(attrs={'class':'form-control','placeholder':'Apartment or suite'}),
        }
