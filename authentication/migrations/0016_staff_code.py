# Generated by Django 5.1 on 2024-10-26 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_remove_staff_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='code',
            field=models.CharField(default=459678, max_length=6, unique=True),
            preserve_default=False,
        ),
    ]