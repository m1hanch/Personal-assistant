# Generated by Django 5.0.1 on 2024-01-14 15:11

import file_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_manager", "0002_uploadedfile_folder"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadedfile",
            name="file",
            field=models.FileField(upload_to=file_manager.models.get_upload_path),
        ),
    ]