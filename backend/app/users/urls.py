from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'users'
urlpatterns = [
    path('get_address/', views.get_address),
    path('set_address/', views.set_address),
    path('get_settings/', views.get_settings),
    path('set_settings/', views.set_settings),
    path('get_email/', views.get_email),
    path('get_services/', views.get_services)
]