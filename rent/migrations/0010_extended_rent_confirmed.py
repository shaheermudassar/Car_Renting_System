# Generated by Django 5.0.3 on 2024-03-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0009_rent_extended_rent_rent_is_extended_extended_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='extended_rent',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]