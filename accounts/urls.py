from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('login',views.login_view, name='login'),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('profile', views.profile_view, name= 'profile')
]