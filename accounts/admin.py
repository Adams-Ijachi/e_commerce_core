from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.



class EmployeeAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name','last_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
   
 
    pass

admin.site.register(User, EmployeeAdmin)
admin.site.register(Agent)
admin.site.register(Customer)

