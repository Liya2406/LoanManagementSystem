from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import my_applications, edit_application, delete_application


urlpatterns = [
     path('',views.home,name="home"),
     path('signup',views.signup,name="signup"),
     path('signin',views.signin,name="signin"),
     path('index1',views.index1,name="index1"),
     path('header',views.header,name="header"),
     path('ploan',views.ploan,name="ploan"),
     path('loanreg',views.loanreg,name="loanreg"),
     path('personalpage', views.personalpage,name="personalpage"),
     path('success', views.success_page, name='success_page'),
     path('my-applications/', my_applications, name='my_applications'),
     path('edit-application/<int:application_id>/', edit_application, name='edit_application'),
     path('delete-application/<int:application_id>/', delete_application, name='delete_application'),
     path('view/<int:application_id>/', views.view_application, name='view_application'),  # New view URL
     # path('applications/', views.view_applications, name='view_applications'),  # View all applications
     path('staff-login/', views.staff_login, name='staff_login'),
     path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
     path('loan_applications/', views.loan_applications, name='loan_applications'),
     path('update_application/<int:application_id>/', views.update_application_status, name='update_application_status'),
     path('view-application/<int:application_id>/', views.view_application_staff, name='view_application_staff'),
     path('rejection-details/<int:application_id>/', views.rejection_details, name='rejection_details'), 
     path('loan-agreement/<int:application_id>', views.loan_agreement_view, name='loan_agreement_view'),
     path('emi',views.emi,name="emi"),
     path('upload_agreement/<str:application_number>/', views.upload_agreement_pdf, name='upload_agreement_pdf'),
     path('applications/', views.application_list_view, name='application_list'),
     path('loan-overview/<int:application_id>/', views.loan_overview_view, name='loan_overview'),
     path('mark_payment_as_paid/<int:payment_id>/', views.mark_payment_as_paid, name='mark_payment_as_paid'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

