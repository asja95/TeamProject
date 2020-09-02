from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('artist_list/<int:artist_id>', views.artist_list, name='artist_list'),
    path('genre/', views.genre, name='genre'),
    path('chart/', views.chart, name='chart'),
]