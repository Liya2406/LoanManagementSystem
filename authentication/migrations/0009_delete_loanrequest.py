# Generated by Django 5.1.1 on 2024-10-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_merge_20241023_1406'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoanRequest',
        ),
    ]
