from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class CustommAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        print(password)
        other_fields.setdefault('is_staff',  True)
        other_fields.setdefault('is_superuser',  True)
        other_fields.setdefault('is_active',  True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True.')
        
        return self.create_user(email, first_name, last_name, password, **other_fields)


    def create_user(self, email, first_name, last_name, password=None, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_customer', True)
        email = self.normalize_email(email)
        user = self.model( email=email, first_name = first_name,last_name=last_name,**other_fields)
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user
      
        


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustommAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

class Agent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(verbose_name='Profile Image',upload_to='img/profile_image/agent', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number',null=True, blank=True)
    home_address = models.CharField(max_length=100, verbose_name='Home Address',null=True, blank=True)
    market_location = models.CharField(max_length=100, verbose_name='Market / Location Designation',null=True, blank=True)

    def __str__(self):
        return self.user.email

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(verbose_name='Customer Image',upload_to='img/profile_image/customer', null=True, blank=True)

    def __str__(self):
        return self.user.email