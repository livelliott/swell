from django.urls import path
from . import views

app_name = 'envelope'
# specific for members application
urlpatterns = [
    path('create/', views.create_envelope, name='envelope_create'),
]
