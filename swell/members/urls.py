from django.contrib import admin
from django.urls import include, path
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

app_name = 'members'
# route users that comes in via 127.0.0.1:8000/...
urlpatterns = [
    path('', views.landing, name="members_landing"),
    path('login/', views.login_user, name="login_users"),
    path('logout/', views.logout_user, name="logout_users"),
    path('register/', views.register_users, name="register_users"),
]