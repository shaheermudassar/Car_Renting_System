# Generated by Django 5.0.3 on 2024-04-03 11:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0017_alter_carimages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='logo',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
    ]
