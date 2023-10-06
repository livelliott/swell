from django.urls import path
from . import views

# specific for members application
urlpatterns = [
    path('members/', views.members, name='members'),
]