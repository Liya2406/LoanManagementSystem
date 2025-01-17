# Generated by Django 5.1 on 2024-11-04 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False)),
                ('pdf_file', models.FileField(upload_to='agreements/')),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('rejection_comments', models.TextField(blank=True, null=True)),
                ('loan_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='applications.loanapp')),
            ],
        ),
    ]
