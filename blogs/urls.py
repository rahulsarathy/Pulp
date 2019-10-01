from django.urls import include, path
from rest_framework import routers

from . import views


app_name = 'blogs'

urlpatterns = [
    path('', views.get_blogs),
    path('subscribe/', views.subscribe),
    path('check_sub_status/', views.check_sub_status),
    path('unsubscribe/', views.unsubscribe),
    path('landing_blogs', views.get_landing_blogs),
    path('get_subscriptions', views.get_subscriptions)
]