# Generated by Django 5.1.1 on 2024-10-23 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_loanapp_loan_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapp',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='loanapp',
            name='down_payment',
        ),
        migrations.RemoveField(
            model_name='loanapp',
            name='rent_mortgage',
        ),
    ]
