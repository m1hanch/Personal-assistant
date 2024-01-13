from django.urls import path

from .views import file_upload, file_list, list_s3_contents, view_folder_contents

app_name = 'file_manager'

urlpatterns = [
    path('upload/', file_upload, name='file_upload'),
    path('list/', file_list, name='file_list'),
    path('list_s3_contents/', list_s3_contents, name='list_s3_contents'),
    path('view_folder_contents/<str:folder_name>/', view_folder_contents, name='view_folder_contents'),
]
