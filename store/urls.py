from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('',views.home_view, name='home')
]