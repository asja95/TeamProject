from django.urls import path
from . import views

app_name = 'interest'
urlpatterns = [
    path('interest/', views.interest, name='interest'),
]