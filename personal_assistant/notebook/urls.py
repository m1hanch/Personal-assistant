from django.urls import path
from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('add_note/', views.add_note, name='add_note'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    path('delete/<int:note_id>', views.delete_note, name='delete'),
    # path('search/', views.search_notes, name='search_notes'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('search_and_sort/', views.search_and_sort_notes, name='search_and_sort_notes'),

    
    
    
]