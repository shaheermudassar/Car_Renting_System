# Generated by Django 4.2.6 on 2024-01-20 07:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_car_model_car_year_of_manufacture'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='specification',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='This is the specification', null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='This is the description', null=True),
        ),
    ]
