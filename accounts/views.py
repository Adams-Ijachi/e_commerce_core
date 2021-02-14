from django.contrib import messages
from django.shortcuts import render , redirect, reverse
from .forms import UserCreateForm,UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from .models import User
from accounts.emailauth import EmailAuthentication

# Create your views here.
def login_view(request):
    form  = UserLoginForm(request, data = request.POST or None)
   
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_ = EmailAuthentication.authenticate(request,username=email, password=password)
        print(user_)
        if user_:
            login(request, user_)
            return redirect(reverse('accounts:profile'))
        messages.error(request, 'Email or Password incorrect')
        return redirect(reverse('accounts:login'))

    print(form.errors)
    context = {"form":form, "btn_label":"Login", "title":"Login"}
    return render(request, 'profiles/pages/login.html', context)

def profile_view(request):
    return render(request, 'profiles/pages/home_dashboard.html')

