from django import forms
from .models import User
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from random import choice


class UserCreateForm(UserCreationForm):
    username = None
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'password',}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'confirm-password'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ( 'email','first_name', 'last_name','password1')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    



   
   
class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'password', 'placeholder':'Password'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email','password')
    field_order = ['email','password']
       
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
        self.fields.pop('username')
        