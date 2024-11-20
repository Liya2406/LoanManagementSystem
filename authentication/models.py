from django.db import models
from loan.models import Loan
from django.utils import timezone
import random

# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.EmailField()
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    def __str__(self):
        return self.name

from django.db import models


class Staff(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    code=models.CharField(max_length=6, unique=True)
    # otp = models.CharField(max_length=6, blank=True, null=True)
    # Additional fields as necessary
    
    def __str__(self):
        return self.name
    

