from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def EMI(request):
    # return HttpResponse("welcome")
    return render(request,'calculator/emi.html')
# views.py in your app (e.g., home)

 # Import your Loan model
 # Pass loans to the template
# def home(request):
#     loans = Loan.objects.all()
#     print(loans)  # Check what loans are being fetched
#     return render(request, 'authentication/home.html', {'loans': loans})
