from django.urls import path

from .views import file_upload, file_list, list_s3_contents, view_folder_contents, create_folder, delete_file, delete_folder

app_name = 'file_manager'

urlpatterns = [
    path('upload/', file_upload, name='file_upload'),
    path('delete_file/', delete_file, name='delete_file'),
    path('create_folder/', create_folder, name='create_folder'),
    path('delete_folder/', delete_folder, name='delete_folder'),
    path('list/', file_list, name='file_list'),
    path('list_s3_contents/', list_s3_contents, name='list_s3_contents'),
    path('view_folder_contents/<str:folder_name>/', view_folder_contents, name='view_folder_contents'),
]
