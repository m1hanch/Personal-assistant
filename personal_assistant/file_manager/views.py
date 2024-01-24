from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
import boto3
from botocore.exceptions import ClientError
import os
from .forms import FileUploadForm
from .models import UploadedFile

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION_NAME"),
    endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
)


def get_category(file_extension):
    video_extensions = ['.mp4', '.avi', '.mkv']
    music_extensions = ['.mp3', '.wav', '.ogg', 'm4a']
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    if file_extension.lower() in video_extensions:
        return 'VIDEO'
    elif file_extension.lower() in music_extensions:
        return 'MUSIC'
    elif file_extension.lower() in image_extensions:
        return 'IMAGE'
    else:
        return 'OTHER'


@login_required
def file_upload(request):
    folders = UploadedFile.objects.filter(user=request.user).values_list('folder', flat=True).distinct()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        form.fields['folder'].queryset = UploadedFile.objects.filter(user=request.user)
        if form.is_valid():
            folder = form.cleaned_data['folder']
            file = form.cleaned_data['file']

            if not folder or folder not in folders:
                folder = None

            file_name, file_extension = os.path.splitext(file.name)
            key = file.name if not folder else f'{folder}/{file.name}'
            s3.upload_fileobj(file, 'webproject8', key)
            category = get_category(file_extension)
            UploadedFile.objects.create(folder=folder, file=key, category=category, user=request.user)

            return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})
    else:
        form = FileUploadForm()
        form.fields['folder'].queryset = UploadedFile.objects.filter(user=request.user)

    return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})


@login_required
def create_folder(request):
    folders = UploadedFile.objects.filter(user=request.user).values_list('folder', flat=True).distinct()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        folder = request.POST.get('folder', '')

        if folder and not UploadedFile.objects.filter(folder=folder).exists():
            UploadedFile.objects.create(folder=folder, user=request.user)
            s3.put_object(Bucket='webproject8', Key=f'{folder}/')

            return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})

    else:
        form = FileUploadForm()

    return render(request, 'file_manager/file_upload.html', {'form': form, 'folders': folders})


@login_required
def delete_folder(request):
    folders = UploadedFile.objects.filter(user=request.user).values_list('folder', flat=True).distinct()
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')

        try:
            objects_to_delete = [{'Key': f"{folder_name}/{obj.file.name.split('/')[-1]}"} for obj in
                                 UploadedFile.objects.filter(folder=folder_name, user=request.user) if obj.file.name]
            if objects_to_delete:
                s3.delete_objects(Bucket='webproject8', Delete={'Objects': objects_to_delete})
            s3.delete_object(Bucket='webproject8', Key=f"{folder_name}/")
            UploadedFile.objects.filter(folder=folder_name, user=request.user).delete()

        except ClientError as e:
            print(f"Error deleting folder from S3: {e}")

        return render(request, 'file_manager/delete_folder.html', {'folders': folders})
    else:
        return render(request, 'file_manager/delete_folder.html', {'folders': folders})


@login_required
def delete_file(request, file_id=None):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file_to_delete = get_object_or_404(UploadedFile, id=file_id)
        file_to_delete.delete()
        s3.delete_object(Bucket='webproject8', Key=file_to_delete.file.name)
        folders = UploadedFile.objects.values_list('folder', flat=True).distinct()
        form = FileUploadForm()
        form.fields['folder'].queryset = folders

        return render(request, 'file_manager/file_delete.html',
                      {'form': form, 'files': UploadedFile.objects.filter(user=request.user)})

    if not file_id:
        files = UploadedFile.objects.filter(user=request.user)
        return render(request, 'file_manager/file_delete.html', {'files': files})
    else:
        file_to_delete = get_object_or_404(UploadedFile, id=file_id)
        return render(request, 'file_manager/file_delete.html')


@login_required
def move_file(request):
    files = UploadedFile.objects.filter(user=request.user)
    folders = UploadedFile.objects.filter(user=request.user).values_list('folder', flat=True).distinct()

    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        target_folder = request.POST.get('target_folder')
        file_to_move = UploadedFile.objects.get(id=file_id, user=request.user)
        old_key = file_to_move.file.name
        file_name, file_extension = os.path.splitext(file_to_move.file.name.split('/')[-1])

        if target_folder:
            new_key = f"{target_folder}/{file_name}{file_extension}"
        else:
            new_key = f"{file_name}{file_extension}"

        s3.copy_object(Bucket='webproject8', CopySource={'Bucket': 'webproject8', 'Key': old_key}, Key=new_key)
        s3.delete_object(Bucket='webproject8', Key=old_key)
        file_to_move.folder = target_folder
        file_to_move.file = new_key
        file_to_move.save()

        return render(request, 'file_manager/move_file.html', {'files': files, 'folders': folders})

    return render(request, 'file_manager/move_file.html', {'files': files, 'folders': folders})


@login_required
def download_file(request, file_id=None):
    files = UploadedFile.objects.all()

    if file_id:
        file_model = get_object_or_404(UploadedFile, pk=file_id)
        response = HttpResponse(file_model.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_model.file.name}"'
        return response

    return render(request, 'file_manager/download_file.html', {'files': files})


@login_required
def file_list(request):
    files_by_category = {
        'VIDEO': UploadedFile.objects.filter(category='VIDEO', user=request.user),
        'MUSIC': UploadedFile.objects.filter(category='MUSIC', user=request.user),
        'IMAGE': UploadedFile.objects.filter(category='IMAGE', user=request.user),
        'OTHER': UploadedFile.objects.filter(category='OTHER', user=request.user),
    }

    return render(request, 'file_manager/file_list.html', {'files_by_category': files_by_category})


@login_required
def list_s3_contents(request):
    bucket_name = 'webproject8'
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    folders = [prefix['Prefix'] for prefix in response.get('CommonPrefixes', [])]
    files = [obj['Key'] for obj in response.get('Contents', [])]

    if not folders:
        return render(request, 'file_manager/s3_list.html', {'folders': [], 'files': files})

    folder_urls = [reverse('file_manager:view_folder_contents', kwargs={'folder_name': folder.strip('/')})
                   for folder in folders]

    return render(request, 'file_manager/s3_list.html', {'folders': zip(folders, folder_urls), 'files': files})
