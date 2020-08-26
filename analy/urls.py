from django.urls import path
from . import views

app_name = 'analy'
urlpatterns = [
    path('upload/', views.upload, name='upload'),
]

