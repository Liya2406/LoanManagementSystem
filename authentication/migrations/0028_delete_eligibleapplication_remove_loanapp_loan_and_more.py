# Generated by Django 5.1 on 2024-11-03 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0027_eligibleapplication'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EligibleApplication',
        ),
        migrations.RemoveField(
            model_name='loanapp',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='loanapp',
            name='user',
        ),
        migrations.DeleteModel(
            name='RejectedApplications',
        ),
        migrations.DeleteModel(
            name='LoanApp',
        ),
    ]
