# Generated by Django 5.1 on 2024-10-25 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_remove_loanapp_comments_remove_loanapp_down_payment_and_more'),
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapp',
            name='loan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.loan'),
        ),
    ]
