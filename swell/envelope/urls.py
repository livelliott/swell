from django.urls import path
from . import views

app_name = 'envelope'
# specific for members application
urlpatterns = [
    path('create/', views.envelope_create, name='envelope_create'),
    path('envelope-create-prompts/', views.envelope_create_prompts, name='envelope_create_prompts'),
    path('envelope-create-invite/', views.envelope_create_invite, name='envelope_create_invite'),
    path('create-envelope-success/', views.envelope_create_success, name='envelope_create_success'),
]
