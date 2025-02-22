# Generated by Django 5.1.2 on 2024-12-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0011_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('started', 'Started'), ('ended', 'Ended'), ('cancelled', 'Cancelled')], default='started', max_length=20),
        ),
    ]
