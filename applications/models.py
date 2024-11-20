from django.db import models
from django.utils import timezone
import random
from loan.models import Loan
from authentication.models import Register

# Create your models here.
class LoanApp(models.Model):
    application_number = models.CharField(max_length=6, unique=True, blank=True)

    # Override save method to generate a unique 6-digit application number
    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = self.generate_unique_application_number()
        super().save(*args, **kwargs)

    def generate_unique_application_number(self):
        while True:
            number = str(random.randint(100000, 999999))  # Generate a random 6-digit number
            if not LoanApp.objects.filter(application_number=number).exists():
                return number
    LOAN_AMOUNT_CHOICES = [
        (100000, '100000'),
        (500000, '500000'),  # Correctly formatted
        (1000000, '1000000'),  # 10 Lakhs
        # Add more options as needed
    ]
    
    loan_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=LOAN_AMOUNT_CHOICES,
        default=100000  # Set a default value that exists in the choices
    )
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.CharField(max_length=100)
    title = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    marital_status = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    residence_duration = models.CharField(max_length=10)
    employer = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    experience = models.CharField(max_length=10)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    bank_address = models.CharField(max_length=255)
    bank_phone = models.CharField(max_length=15)
    consent = models.BooleanField()
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    # File upload fields
    document1 = models.FileField(upload_to='documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='documents/', null=True, blank=True)
    document3 = models.FileField(upload_to='documents/', null=True, blank=True)

    STATUS_CHOICES = [
        ('Submitted','Submitted'),
        ('Pending', 'Pending'),
        ('Eligible', 'Eligible'),
        ('Rejected', 'Rejected'),
    ]

    Application_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    Add_rejection_comments = models.TextField(blank=True, null=True)  # To capture rejection reasons
    
    # Add a method to mark the application as Eligible or rejected
    def submitted(self):
        self.status = 'Submitted'
        self.save()

    def pending(self):
        self.status = 'pending'
        self.save()

    def eligible(self):
        self.status = 'Eligible'
        self.save()

    def reject(self, comments):
        self.status = 'Rejected'
        self.rejection_comments = comments
        self.save()
    

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.loan_amount} for {self.loan_purpose} (Status: {self.Application_status}{self.application_number})"



class RejectedApplications(models.Model):
    application_number = models.CharField(max_length=6)
    loan_purpose = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rejection_comments = models.TextField(blank=True, null=True)
    rejection_date = models.DateTimeField(auto_now_add=True)
    rejected_by_employee_id = models.CharField(max_length=50)  # Field for staff ID
    rejected_by_name = models.CharField(max_length=100)  # Field for staff name
    

    def __str__(self):
        return f"Rejected Application {self.application_number} by staff {self.rejected_by_name} "
    
from django.db import models
from django.contrib.auth.models import User


class EligibleApplication(models.Model):
    application_number = models.CharField(max_length=6)
    loan_purpose = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    verified_date = models.DateTimeField(auto_now_add=True)
    verified_by_employee_id = models.CharField(max_length=50)  # Field for staff ID
    verified_by_name = models.CharField(max_length=100)  # Field for staff name
    

    def __str__(self):
        return f"verified Application {self.application_number} - by staff {self.verified_by_name}"
    

from django.db import models

class Agreement(models.Model):
    application_number = models.CharField(max_length=6)
    pdf_file = models.FileField(upload_to='agreements/')
    status = models.CharField(
        max_length=10,
        choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'),('Pending','Pending')],
        default='Pending'
    )
    rejection_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Agreement for Application {self.application_number}"

class LoanPayment(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    loan = models.ForeignKey(LoanApp, related_name="payments", on_delete=models.CASCADE)
    month = models.PositiveIntegerField()  # 1 to 60 for each month in the 5-year period
    year = models.PositiveIntegerField()  # The year of the payment (1 to 5)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Default status is Pending
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Payment amount field

    def __str__(self):
        return f"Payment for Loan {self.loan.application_number} Month: {self.month} Year: {self.year} Status: {self.status}"