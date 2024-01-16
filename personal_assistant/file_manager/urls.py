
from django.urls import path

from .views import file_upload, file_list, create_folder, delete_file, delete_folder, move_file, download_file, list_s3_contents

app_name = 'file_manager'

urlpatterns = [
    path('upload/', file_upload, name='file_upload'),
    path('delete_file/', delete_file, name='delete_file'),
    path('create_folder/', create_folder, name='create_folder'),
    path('delete_folder/', delete_folder, name='delete_folder'),
    path('move_file/', move_file, name='move_file'),
    path('download_file/<int:file_id>/', download_file, name='download_file'),
    path('list/', file_list, name='file_list'),
    path('list_s3_contents/', list_s3_contents, name='list_s3_contents'),
]
