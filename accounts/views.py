from django.contrib import messages
from django.shortcuts import render , redirect, reverse 
from .forms import UserCreateForm,UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from .models import User ,  Customer
from accounts.emailauth import EmailAuthentication
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request, *args, **kwargs):
    form  = UserLoginForm(request, data = request.POST or None)
   
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_ = EmailAuthentication.authenticate(request,username=email, password=password)
        if user_:
            login(request, user_)
            return redirect(reverse('accounts:profile'))
        messages.error(request, 'Email or Password incorrect')
        return redirect(reverse('accounts:login'))

    context = {"form":form, "btn_label":"Login", "title":"Login"}
    return render(request, 'profiles/pages/login.html', context)

def register_view(request, *args, **kwargs):
    form  = UserCreateForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        customer = Customer.objects.get_or_create(user=user)
        user.set_password(form.cleaned_data.get("password2"))
        return redirect(reverse('accounts:login'))
    context = {"form":form, "btn_label":"Login", "title":"Register"}
    return render(request, 'profiles/pages/register.html', context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect('accounts:login')
    return redirect(reverse('core:home'))

  

@login_required
def profile_view(request):
    return render(request, 'profiles/pages/home_dashboard.html')

