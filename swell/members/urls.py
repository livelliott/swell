from django.contrib import admin
from django.urls import include, path
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

app_name = 'members'
# route users that comes in via 127.0.0.1:8000/...
urlpatterns = [
    path('', views.login_user, name="login_users"),
]