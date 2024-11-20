from django.contrib import admin
from .models import RejectedApplications
from .models import EligibleApplication
from .models import LoanApp
from .models import Agreement
from .models import LoanPayment
# Register your models here.
admin.site.register(RejectedApplications)
admin.site.register(EligibleApplication)
admin.site.register(LoanApp)
admin.site.register(Agreement)
admin.site.register(LoanPayment)