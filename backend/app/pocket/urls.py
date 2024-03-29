from django.urls import include, path
from rest_framework import routers

from . import views


app_name = 'pocket'

urlpatterns = [
    path('request_pocket', views.request_pocket),
    path('authenticate_pocket', views.authenticate_pocket, name='authenticate_pocket'),
    path('sync_pocket', views.sync_pocket),
    path('remove_pocket', views.remove_pocket),
]