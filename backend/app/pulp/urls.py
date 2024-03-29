"""pulp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, re_path
from pulp import views

urlpatterns = [
  path('secret_admin1/', admin.site.urls),

  # landing page switcher
  path('', views.redirect_to_landing, name='redirect_to_landing'),
  path('landing/', views.landing, name='landing'),
  path('pricing/', views.landing, name='pricing'),
  path('faq/', views.landing, name='faq'),
  path('publishers/', views.landing, name='publishers'),

  # signed in switcher
  path('reading_list/', views.switcher, name='switcher'),
  path('delivery/', views.switcher, name='delivery'),
  path('profile/', views.switcher, name='profile'),
  path('archive/', views.switcher, name='archive'),
  path('payments/', views.switcher, name='payments'),
  path('blogs/', views.switcher, name='blogs'),
  path('articles/', include('articles.urls')),

  # api endpoints
  path('api/users/', include('users.urls')),
  path('api/reading_list/', include('reading_list.urls')),
  path('api/payments/', include('payments.urls')),
  path('api/instapaper/', include('instapaper.urls')),
  path('api/pocket/', include('pocket.urls')),
  path('api/twitter/', include('twitter.urls')),
  path('api/blogs/', include('blogs.urls')),

  path('twitter/', views.twitter),

  # django 3rd party
  path('accounts/', include('allauth.urls')),
  path('ready/', include('health_check.urls')),
]

handler404 = views.error_404
