# Generated by Django 5.1.2 on 2024-10-16 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_location_alter_car_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='days',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
