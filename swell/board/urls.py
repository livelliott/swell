from django.urls import path
from . import views

app_name = 'board'
# specific for members application
urlpatterns = [
    path('home/', views.home_page, name='board_home'),
]
