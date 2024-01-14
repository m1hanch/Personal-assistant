from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import boto3
import os
from .forms import FileUploadForm
from .models import UploadedFile


def file_upload(request):
    folders = UploadedFile.objects.values_list('folder', flat=True).distinct()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})
    else:
        form = FileUploadForm()
        form.fields['folder'].queryset = folders

    return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})


def create_folder(request):
    folders = UploadedFile.objects.values_list('folder', flat=True).distinct()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        folder = request.POST.get('folder', '')

        if folder and not UploadedFile.objects.filter(folder=folder).exists():
            UploadedFile.objects.create(folder=folder)

            s3 = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_S3_REGION_NAME"),
                endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
            )

            s3.put_object(Bucket='webproject8', Key=f'{folder}/')

            return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})

    else:
        form = FileUploadForm()

    return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})


def delete_folder(request):
    folders = UploadedFile.objects.values_list('folder', flat=True).distinct()
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_S3_REGION_NAME"),
            endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
        )

        s3.delete_objects(Bucket='webproject8', Delete={'Objects': [{'Key': f"{folder_name}/"}]})

        UploadedFile.objects.filter(folder=folder_name).delete()

        return render(request, 'file_manager/delete_folder.html', {'folders': folders})
    else:
        return render(request, 'file_manager/delete_folder.html', {'folders': folders})


def delete_file(request, file_id=None):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file_to_delete = get_object_or_404(UploadedFile, id=file_id)

        file_to_delete.delete()

        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_S3_REGION_NAME"),
            endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
        )
        s3.delete_object(Bucket='webproject8', Key=file_to_delete.file.name)

        folders = UploadedFile.objects.values_list('folder', flat=True).distinct()
        form = FileUploadForm()
        form.fields['folder'].queryset = folders

        return render(request, 'file_manager/file_delete.html', {'form': form, 'files': UploadedFile.objects.all()})

    if not file_id:
        files = UploadedFile.objects.all()
        return render(request, 'file_manager/file_delete.html', {'files': files})
    else:
        file_to_delete = get_object_or_404(UploadedFile, id=file_id)
        return render(request, 'file_manager/file_delete.html')


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

    objects = s3.list_objects_v2(Bucket='webproject8', Prefix=folder_name)['Contents']
    folder_contents = [obj['Key'] for obj in objects]
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

    if not folders:
        return render(request, 'file_manager/s3_list.html', {'folders': [], 'files': files})

    folder_urls = [reverse('file_manager:view_folder_contents', kwargs={'folder_name': folder.strip('/')})
                   for folder in folders]

    return render(request, 'file_manager/s3_list.html', {'folders': zip(folders, folder_urls), 'files': files})
