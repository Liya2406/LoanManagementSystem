# Generated by Django 5.1 on 2024-10-26 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_staff_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='otp',
        ),
    ]
