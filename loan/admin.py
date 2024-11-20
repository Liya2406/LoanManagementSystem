from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Loan

class LoanAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

admin.site.register(Loan, LoanAdmin)
