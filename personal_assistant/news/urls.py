from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('technology/', views.tech_news, name='tech_news'),
    path('environment/', views.science_news, name='environment_news'),
    path('sports/', views.sports_news, name='sports_news'),
    path('politics/', views.politics_news, name='politics_news'),
]