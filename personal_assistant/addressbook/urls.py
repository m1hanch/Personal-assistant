from django.urls import path

from . import views

app_name = 'addressbook'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_contact, name='add_contact'),
]