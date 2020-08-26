from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('video/', views.video, name='video'),
    path('fifth/', views.fifth, name='fifth'),
    path('chart/', views.chart, name='chart'),
]