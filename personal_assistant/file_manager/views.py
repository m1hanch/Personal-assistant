from django.shortcuts import render, redirect
from django.urls import reverse
import boto3
import os
from .forms import FileUploadForm
from .models import UploadedFile


def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('file_list') # TODO непрацює повернення на 'file_list', доробити або забити
    else:
        form = FileUploadForm()
    return render(request, 'file_manager/file_upload.html', {'form': form})


def file_list(request):
    buckets = UploadedFile.objects.all()
    return render(request, 'file_manager/file_list.html', {'files': buckets})


def view_folder_contents(request, folder_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
    )

    # Отримайте список об'єктів у вказаній папці
    objects = s3.list_objects_v2(Bucket='webproject8', Prefix=folder_name)['Contents']
    folder_contents = [obj['Key'] for obj in objects]

    # Отримати URL для view_list_s3_contents
    list_s3_contents_url = reverse('file_manager:list_s3_contents')

    return render(request, 'file_manager/folder_contents.html',
                  {'folder_contents': folder_contents, 'folder_name': folder_name,
                   'list_s3_contents_url': list_s3_contents_url})


def list_s3_contents(request):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
    )

    bucket_name = 'webproject8'
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    folders = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]
    files = [obj['Key'] for obj in response.get('Contents', [])]

    # Додамо обробку порожнього списку folders
    if not folders:
        return render(request, 'file_manager/s3_list.html', {'folders': [], 'files': files})

    # Отримуємо URL для кожної папки
    folder_urls = [reverse('file_manager:view_folder_contents', kwargs={'folder_name': folder.strip('/')})
                   for folder in folders]

    return render(request, 'file_manager/s3_list.html', {'folders': zip(folders, folder_urls), 'files': files})
