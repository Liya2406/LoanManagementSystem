# Generated by Django 5.1 on 2024-10-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0025_rejectedapplications_rejected_by_employee_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapp',
            name='Application_status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Pending', 'Pending'), ('Eligible', 'Eligible'), ('Rejected', 'Rejected')], default='submitted', max_length=10),
        ),
    ]
