from django.urls import path
from . import views

app_name = 'board'
# specific for members application
urlpatterns = [
    path('home/', views.home_page, name='board_home'),
    path('envelope/<str:envelope_id>/', views.envelope, name='board_envelope'),
    path('envelope/<str:envelope_id>/members', views.envelope_members, name='board_envelope_members')
]
