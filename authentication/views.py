from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from loan.models import Loan
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import  Register
from .models import Staff
from applications.models import LoanApp,RejectedApplications,EligibleApplication,Agreement,LoanPayment
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    loans = Loan.objects.all()
    print(loans)  # Check what loans are being fetched
    return render(request, 'authentication/home.html', {'loans': loans})
def success_page(request):
    return render(request, 'success.html')
def signup(request):
    if request.method=="POST":
        name=request.POST["name"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        username=request.POST["uname"]
        password=request.POST["password"]
        myreg=Register(name=name,phone=phone,email=email,username=username,password=password)
        myreg.save()
        return redirect('signin')
    return render(request,'authentication/signup.html')
def signin(request):
    if request.method=="POST":
        username=request.POST["uname"]
        password=request.POST["password"]
        user=Register.objects.filter(username=username,password=password).first()
        if user is None:
            messages.error(request, 'invalid password or user name')
            return redirect('signin')
        else:
            request.session['uname']=username
            return redirect('personalpage')
    return render(request, 'authentication/signin.html')

def index1(request):
    return render(request,"authentication/index1.html")
def header(request):
    return render(request,"authentication/header.html")
def ploan(request):
    return render(request,"authentication/ploan.html")

@login_required
def loanreg(request):
    if request.method == 'POST':
        username = request.session.get('uname')
        user = Register.objects.filter(username=username).first()
        
        # Handle file upload if a document is submitted
        document1 = request.FILES.get('document1', None)
        document2 = request.FILES.get('document2', None)
        document3 = request.FILES.get('document3', None)

        print("Document 1:", document1)
        print("Document 2:", document2)
        print("Document 3:", document3)

        # Create LoanApp instance and save
        loan_app = LoanApp(
            loan_amount=request.POST['loan_amount'],
            annual_income=request.POST['annual_income'],
            loan_purpose=request.POST['loan_purpose'],
            title=request.POST.get('title', ''),
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            dob=request.POST['dob'],
            marital_status=request.POST['marital_status'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            address2=request.POST.get('address2', ''),
            city=request.POST['city'],
            state=request.POST['state'],
            zip=request.POST['zip'],
            residence_duration=request.POST['residence_duration'],
            employer=request.POST['employer'],
            occupation=request.POST['occupation'],
            experience=request.POST['experience'],
            monthly_income=request.POST['monthly_income'],
            # rent_mortgage=request.POST.get('rent_mortgage', None),
            # down_payment=request.POST.get('down_payment', None),
            # comments=request.POST.get('comments', ''),
            bank_name=request.POST['bank_name'],
            account_number=request.POST['account_number'],
            bank_address=request.POST['bank_address'],
            bank_phone=request.POST['bank_phone'],
            user=user,
            document1=document1,  # First image
            document2=document2,  # Second image
            document3=document3,  # Third image
            consent=request.POST.get('consent') == 'on'  # Handling checkbox
        )

        loan_app.save()
        # return HttpResponse("Loan application submitted successfully!")
        messages.success(request, "Loan application submitted successfully!")
        return redirect('personalpage')
    loan_title = request.GET.get('loan_title', '') 
    return render(request, 'loans/loanreg.html', {'loan_title': loan_title}) 


# def personalpage(request):
#     loans = Loan.objects.all()
#     print(loans)  # Check what loans are being fetched
#     return render(request, 'loans/personalpage.html', {'loans': loans})


def personalpage(request):
    username = request.session.get('uname')
    user = get_object_or_404(Register, username=username)  # Get the logged-in user

    # Fetch all available loans
    loans = Loan.objects.all()

    # Check if the user has an existing loan application
    # has_applied = LoanApp.objects.filter(user=user).exists()
    #     # Retrieve the user's latest loan application if one exists
    # loan_app = LoanApp.objects.filter(user=user).order_by('-id').first()
     # Retrieve the user's latest loan application if one exists
    loan_app = LoanApp.objects.filter(user=user).order_by('-id').first()
    has_applied = loan_app is not None  # Check if the user has applied
    previous_application_status = loan_app.Application_status if loan_app else None  # Get status if exists
    
    if loan_app:
        # Add the application number to the success message
        messages.success(request, f"Your Application Number is: {loan_app.application_number}")

    return render(request, 'loans/personalpage.html', {
        'loans': loans,
        'has_applied': has_applied,  # Pass application status to template
        'previous_application_status': previous_application_status # Pass previous application status
        
    })

# Adjust template as needed

def my_applications(request):
    
    if request.method == 'GET':
        username = request.session.get('uname')
        user = Register.objects.filter(username=username).first()
        applications = LoanApp.objects.filter(user=user) if user else []
        agreements_dict = {}
        
        # Fetch all agreements and populate the dictionary
        for agreement in Agreement.objects.all():
            agreements_dict[agreement.application_number] = {
                "status": agreement.status,
                "rejection_comment": agreement.rejection_comments
            }
        return render(request, 'my_applications.html', {
            'applications': applications,
            'agreements_dict': agreements_dict
        })
    
def edit_application(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)

    if application.dob:
        application.dob = application.dob.strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        application.loan_amount = request.POST['loan_amount']
        application.annual_income = request.POST['annual_income']
        application.loan_purpose = request.POST['loan_purpose']
        application.title = request.POST.get('title', application.title)
        application.first_name = request.POST['first_name']
        application.last_name = request.POST['last_name']
        application.dob = request.POST['dob']
        application.email = request.POST['email']
        application.phone = request.POST['phone']
        application.address = request.POST['address']
        application.address2 = request.POST.get('address2', application.address2)
        application.city = request.POST['city']
        application.state = request.POST['state']
        application.zip = request.POST['zip']
        application.residence_duration = request.POST['residence_duration']
        application.employer = request.POST['employer']
        application.occupation = request.POST['occupation']
        application.experience = request.POST['experience']
        application.monthly_income = request.POST['monthly_income']
        application.marital_status=request.POST['marital_status']
        application.residence_duration=request.POST['residence_duration']
        application.bank_name = request.POST['bank_name']
        application.account_number = request.POST['account_number']
        application.bank_address = request.POST['bank_address']
        application.bank_phone = request.POST['bank_phone']
        
        # Handle document updates if needed
        if request.FILES.get('document1'):
            application.document1 = request.FILES['document1']
        if request.FILES.get('document2'):
            application.document2 = request.FILES['document2']
        if request.FILES.get('document3'):
            application.document3 = request.FILES['document3']
        
        application.save()
        return redirect('my_applications')  # Redirect after editing

    return render(request, 'edit_application.html', {'application': application})


def delete_application(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)
    application.delete()
    return redirect('my_applications')  # Redirect after deletion


def view_application(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)
    return render(request, 'view_application.html', {'application': application})


@csrf_exempt
def staff_login(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        code = request.POST['code']
        try:
            staff = Staff.objects.get(employee_id=employee_id, code=code)
            # Store staff information in session
            request.session['staff_id'] = staff.id
            request.session['staff_name'] = staff.name
            request.session['employee_id'] = staff.employee_id


            return redirect('staff_dashboard')  # Redirect to the staff dashboard
        except Staff.DoesNotExist:
            messages.error(request, 'Invalid Employee ID or Code.')
            return render(request, 'staff/staff_login.html')  # Render login page with the error message
    else:
       return render(request, 'staff/staff_login.html')


# views.py (continued)
@login_required
def staff_dashboard(request):
    # Retrieve staff information from the session
    staff_name = request.session.get('staff_name')
    employee_id = request.session.get('employee_id')
    loans = Loan.objects.all()
    context = {
        'staff_name': staff_name,
        'employee_id': employee_id,
        'loans': loans,
    }

    return render(request, 'staff/staff_dashboard.html',context)  # Render the dashboard with the context
  # Create this template as needed


# views.py
from django.shortcuts import render, redirect

def loan_applications(request):
    applications = LoanApp.objects.all()
    return render(request, 'staff/loan_applications.html', {'applications': applications})



def view_application_staff(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)
    
    # Check if the application has rejection comments
    rejection_comments = application.Add_rejection_comments
    
    return render(request, 'staff/view_application_staff.html', {
        'application': application,
        'rejection_comments': rejection_comments  # Pass rejection comments to the template
    })

def rejection_details(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)
    return render(request, 'staff/rejection_details.html', {
        'application': application
    })


def number_to_words(n):
    # Expanded dictionary to include more numbers
    if isinstance(n, float):
        # Split the number into whole and decimal parts
        whole, decimal = str(n).split(".")
        whole_words = number_to_words(int(whole))
        decimal_words = number_to_words(int(decimal))  # Convert decimal part as well
        return f"{whole_words} and {decimal_words} paise"

    num_words = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
        20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
        60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
        1000: "thousand", 100000: "lakh"
    }

    if isinstance(n, float):
        # Split the number into whole and decimal parts
        whole, decimal = str(n).split(".")
        whole_words = number_to_words(int(whole))
        
        # Process only if the decimal part is non-zero
        if int(decimal) > 0:
            decimal_words = number_to_words(int(decimal))
            return f"{whole_words} and {decimal_words} paise"
        else:
            return whole_words

    if n < 20:
        return num_words[n]
    elif n < 100:
        tens = (n // 10) * 10  # Get the nearest lower ten
        ones = n % 10
        return f"{num_words[tens]}{'' if ones == 0 else ' ' + num_words[ones]}".strip()
    elif n < 1000:
        hundreds = n // 100
        remainder = n % 100
        return f"{num_words[hundreds]} hundred {number_to_words(remainder) if remainder else ''}".strip()
    elif n < 100000:
        thousands = n // 1000
        remainder = n % 1000
        return f"{number_to_words(thousands)} thousand {number_to_words(remainder) if remainder else ''}".strip()
    else:
        lakhs = n // 100000
        remainder = n % 100000
        return f"{number_to_words(lakhs)} lakh {number_to_words(remainder) if remainder else ''}".strip()



from decimal import Decimal
def loan_agreement_view(request, application_id):
    # Retrieve the specific loan application based on the provided application_id
    application = get_object_or_404(LoanApp, id=application_id)
    current_date = timezone.now()
    end_date = current_date.replace(year=current_date.year + 5)
    # Define interest rates by loan purpose
    interest_rates = {
    'home loan': Decimal('0.06'),
    'car loan': Decimal('0.07'),
    'education loan': Decimal('0.08'),
    'health loan': Decimal('0.09'),
    'personal loan': Decimal('0.10')
}

    loan_purpose = application.loan_purpose.lower() 

    interest_rate = interest_rates.get(loan_purpose, interest_rates)

    loan_amount = application.loan_amount
    loan_tenure_years = Decimal('5')  # Assuming a fixed 5-year tenure
    total_interest = loan_amount * interest_rate * loan_tenure_years
    total_amount_payable = loan_amount + total_interest

    # Convert numbers to words
    loan_amount_words = number_to_words(int(loan_amount))  # Convert to int for word conversion
    total_amount_words = number_to_words(int(total_amount_payable))

    # Pass data to the template
    return render(request, 'loans/loan_agreement_view.html', {
        'application': application,
        'current_date': current_date,
        'end_date': end_date,
        'interest_rate': interest_rate * 100,  # For percentage display
        'total_amount_payable': total_amount_payable,
        'loan_amount_words': loan_amount_words,
        'total_amount_words': total_amount_words,
        'loan_purpose' : loan_purpose
    })
def emi(request):
    return render (request,'calculator/emi.html')


def update_application_status(request, application_id):
    application = get_object_or_404(LoanApp, id=application_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'eligible':
            # Mark application as eligible and save it in EligibleApplication
            application.Application_status = 'Eligible'
            application.save()

            # Create and save a record in EligibleApplication
            eligible_app = EligibleApplication(
                application_number=application.application_number,
                loan_purpose=application.loan_purpose,
                first_name=application.first_name,
                last_name=application.last_name,
                email=application.email,
                loan_amount=application.loan_amount,
                verified_date=timezone.now(),
                verified_by_employee_id=request.session.get('employee_id'),  # Fetch employee ID from session
                verified_by_name=request.session.get('staff_name')  # Fetch staff name from session
            )
            eligible_app.save()

            messages.success(request, 'Application has been verified.')
        
        elif action == 'reject':
            rejection_comments = request.POST.get('rejection_comments')
            
            if not rejection_comments.strip():  # Check if comments are empty or whitespace
                messages.error(request, 'Rejection comments are required.')
                return render(request, 'staff/update_application_status.html', {'application': application})

            application.Application_status = 'Rejected'
            application.Add_rejection_comments = rejection_comments
            application.save()

            # Save a copy in RejectedApplications
            rejected_app = RejectedApplications(
                application_number=application.application_number,
                loan_purpose=application.loan_purpose,
                first_name=application.first_name,
                last_name=application.last_name,
                email=application.email,
                loan_amount=application.loan_amount,
                rejection_comments=rejection_comments,
                rejected_by_employee_id=request.session.get('employee_id'),
                rejected_by_name=request.session.get('staff_name'),
                rejection_date=timezone.now()
            )
            rejected_app.save()

            messages.success(request, 'Application was rejected.')

        else:
            application.Application_status = 'Pending'
            application.save()
            messages.info(request, 'Application is under review.')

        return redirect('loan_applications')  # Redirect to the applications page

    return render(request, 'staff/update_application_status.html', {'application': application})

from django.core.exceptions import ObjectDoesNotExist

def upload_agreement_pdf(request, application_number):
    try:
        # Fetch the LoanApp instance
        loan_application = LoanApp.objects.get(application_number=application_number)
    except ObjectDoesNotExist:
        messages.error(request, "Loan application not found.")
        return redirect('personalpage')  # Redirect to an error page or dashboard

    # Fetch the Agreement for this application number, if it exists
    agreement = Agreement.objects.filter(application_number=loan_application.application_number).first()

    if request.method == 'POST' and request.FILES.get('pdf_file'):
        # Check if there's an Agreement and if the status is 'Rejected'
        if agreement and agreement.status == 'Rejected':
            # Delete the rejected agreement
            agreement.delete()
            messages.info(request, f"Rejected agreement for application {application_number} deleted.")
        
        # Create a new Agreement instance with the uploaded PDF
        pdf_file = request.FILES['pdf_file']
        Agreement.objects.create(
            application_number=loan_application.application_number,
            pdf_file=pdf_file,
            status='Pending'  # Set initial status as 'Pending'
        )
        
        messages.success(request, "Agreement uploaded successfully.")
        return redirect('personalpage')  # Redirect to success page

    return render(request, 'my_applications.html', {'loan_application': loan_application, 'agreement': agreement})

from django.shortcuts import render


def application_list_view(request):
    applications = LoanApp.objects.all()
    agreements = Agreement.objects.all()
    
    # Create a dictionary to map application numbers to agreements, including details you want to pass to the template
    agreements_dict = {
        agreement.application_number: {
            "status": agreement.status,
            "rejection_comment": agreement.rejection_comments
        }
        for agreement in agreements
    }
    print("Agreements dictionary with rejection comments:", agreements_dict)

    return render(request, 'my_applications.html', {
        'applications': applications,
        'agreements_dict': agreements_dict
    })


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum
# Import your models

import calendar

def loan_overview_view(request, application_id):
    # Retrieve the specific loan application based on the provided application_id
    application = get_object_or_404(LoanApp, id=application_id)
    current_date = timezone.now()

    # Define interest rates based on loan purposes
    interest_rates = {
        'home loan': Decimal('0.06'),
        'car loan': Decimal('0.07'),
        'education loan': Decimal('0.08'),
        'health loan': Decimal('0.09'),
        'personal loan': Decimal('0.10')
    }

    loan_purpose = application.loan_purpose.lower()

    # Set the interest rate, defaulting to 10% if no match is found
    interest_rate = interest_rates.get(loan_purpose, Decimal('0.10'))

    loan_amount = application.loan_amount
    loan_tenure_years = Decimal('5')  # Assuming a fixed 5-year tenure
    total_interest = loan_amount * interest_rate * loan_tenure_years
    total_amount_payable = loan_amount + total_interest

    # Calculate monthly payment amount
    monthly_payment = total_amount_payable / (loan_tenure_years * 12)

    # Prepare due dates and payment statuses for each month
    due_dates = []
    payments = LoanPayment.objects.filter(loan=application)
    payments_by_month = {payment.month: payment for payment in payments}

    # Start from the current month
    loan_start_date = current_date.replace(day=1)
    start_year = loan_start_date.year
    start_month = loan_start_date.month
    # Loop through each month in the loan tenure (5 years = 60 months)
    for month_num in range(1, int(loan_tenure_years * 12) + 1):
        # Manually calculate year and month
        total_months = start_month + month_num - 1
        year = loan_start_date.year + (total_months // 12)  # Adjust the year
        month = total_months % 12  # Adjust the month (0-11)
        if month == 0:
            month = 12 
            year -= 1 # If month is 0, it means December

        # Get the month name using calendar module
        month_name = calendar.month_name[month]  # month_name[1] = "January"

        # Get the payment for this month if it exists
        payment = payments_by_month.get(month_num)

        due_dates.append({
            'month': month_name,  # Month name instead of number
            'year': year,
            'due_date': f"{year}-{month:02d}-01",  # Format the due date (1st day of each month)
            'status': payment.status if payment else 'Pending',
            'payment_id': payment.id if payment else None,
            'amount': monthly_payment
        })

    # Calculate the progress percentage (how much is paid so far)
    paid_amount = LoanPayment.objects.filter(loan=application, status='Paid').aggregate(total_paid=Sum('amount'))['total_paid'] or Decimal('0')
    progress_percentage = (paid_amount / total_amount_payable) * Decimal('100')

    # Render template with the organized data
    return render(request, 'status.html', {
        'application': application,
        'interest_rate': interest_rate * 100,  # Show as a percentage
        'total_amount_payable': total_amount_payable.quantize(Decimal('0.01')),
        'monthly_payment': monthly_payment.quantize(Decimal('0.01')),
        'due_dates': due_dates,  # Pass due dates with payment statuses and amounts
        'current_date': current_date,
        'progress_percentage': progress_percentage.quantize(Decimal('0.01')),  # Display the progress percentage
    })



def create_loan_payments(application):
    loan_tenure_years = 5  # 5 years
    current_date = timezone.now()  # To set due dates

    for year in range(1, loan_tenure_years + 1):
        for month in range(1, 13):  # 12 months per year
            LoanPayment.objects.create(
                loan=application,
                year=year,
                month=month,
                status='Pending',  # Default status is Pending
            )


from django.http import JsonResponse

# def mark_payment_as_paid(request, payment_id):
#     payment = get_object_or_404(LoanPayment, id=payment_id)
#     payment.status = 'Paid'
#     payment.save()
#     return JsonResponse({'status': 'success'})
def mark_payment_as_paid(request, payment_id):
    # Get the current payment and check its month
    payment = get_object_or_404(LoanPayment, id=payment_id)

    # Find the previous payment month, if any
    previous_payment = LoanPayment.objects.filter(
        loan=payment.loan, month=payment.month - 1
    ).first()

    # Allow payment if it's the first month or the previous payment is already paid
    if previous_payment is None or previous_payment.status == 'Paid':
        payment.status = 'Paid'
        payment.save()
        return JsonResponse({'status': 'success'})
    else:
        # If previous payment isn't paid, prevent current payment
        return JsonResponse({'status': 'error', 'message': 'Previous payment not yet paid.'}, status=400)