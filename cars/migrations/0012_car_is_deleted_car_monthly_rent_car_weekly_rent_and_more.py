# Generated by Django 4.2.6 on 2024-02-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_alter_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='car',
            name='monthly_rent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='car',
            name='weekly_rent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='car',
            name='per_day_rent',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='carimages',
            name='image',
            field=models.ImageField(null=True, upload_to='Car/All_Images/{{self.car.name}}_{{self.model}}_{{self.car.id}}'),
        ),
    ]
