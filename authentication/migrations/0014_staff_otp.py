# Generated by Django 5.1 on 2024-10-26 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_staff_alter_loanapp_loan_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
