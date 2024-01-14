# Generated by Django 5.0.1 on 2024-01-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
                ('image_link', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]