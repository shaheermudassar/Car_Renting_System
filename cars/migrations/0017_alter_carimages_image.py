# Generated by Django 5.0.3 on 2024-04-03 09:23

import cars.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_alter_review_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carimages',
            name='image',
            field=models.ImageField(null=True, upload_to=cars.models.CarImages.upload_to),
        ),
    ]
