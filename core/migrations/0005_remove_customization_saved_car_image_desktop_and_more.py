# Generated by Django 5.0.3 on 2024-03-20 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_customization_main_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customization',
            name='saved_car_image_desktop',
        ),
        migrations.RemoveField(
            model_name='customization',
            name='saved_car_image_mobile',
        ),
    ]
