from django.urls import path
from . import views

app_name = 'interest'
urlpatterns = [
    path('third/', views.third, name='third'),
    path('interest/', views.interest, name='interest'),
]