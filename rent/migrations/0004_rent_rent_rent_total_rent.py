# Generated by Django 4.2.6 on 2024-02-25 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_remove_rent_payment_method_rent_delivery_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='rent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rent',
            name='total_rent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]