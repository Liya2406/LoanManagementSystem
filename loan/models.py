

# Create your models here.
from django.db import models

class Loan(models.Model):
    title = models.CharField(max_length=100)
    required_documents = models.TextField(help_text="List required documents, separated by new lines.")
    eligibility_criteria = models.TextField(help_text="List eligibility criteria, separated by new lines.")
    
    def __str__(self):
        return self.title
