from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from clinic import views as clinic_views

from clinic.views import (
    index,
    patients, add_patient, edit_patient, delete_patient,
    doctors, add_doctor, edit_doctor, delete_doctor,
    appointments, add_appointment, edit_appointment, delete_appointment,
    diagnoses, add_diagnosis, edit_diagnosis, delete_diagnosis,
    treatments, add_treatment, edit_treatment, delete_treatment,
    prescriptions, add_prescription, edit_prescription, delete_prescription,
    bills, add_bill, edit_bill, delete_bill,
    payments, add_payment, edit_payment, delete_payment,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='Home'),
    path('register/', clinic_views.register, name='register'),

    # Login / logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Patients
    path('patients/', patients, name='patients'),
    path('patients/add/', add_patient, name='add_patient'),
    path('patients/<int:pk>/edit/', edit_patient, name='edit_patient'),
    path('patients/<int:pk>/delete/', delete_patient, name='delete_patient'),

    # Doctors
    path('doctors/', doctors, name='doctors'),
    path('doctors/add/', add_doctor, name='add_doctor'),
    path('doctors/<int:pk>/edit/', edit_doctor, name='edit_doctor'),
    path('doctors/<int:pk>/delete/', delete_doctor, name='delete_doctor'),

    # Appointments
    path('appointments/', appointments, name='appointments'),
    path('appointments/add/', add_appointment, name='add_appointment'),
    path('appointments/<int:pk>/edit/', edit_appointment, name='edit_appointment'),
    path('appointments/<int:pk>/delete/', delete_appointment, name='delete_appointment'),

    # Diagnoses
    path('diagnoses/', diagnoses, name='diagnoses'),
    path('diagnoses/add/', add_diagnosis, name='add_diagnosis'),
    path('diagnoses/<int:pk>/edit/', edit_diagnosis, name='edit_diagnosis'),
    path('diagnoses/<int:pk>/delete/', delete_diagnosis, name='delete_diagnosis'),

    # Treatments
    path('treatments/', treatments, name='treatments'),
    path('treatments/add/', add_treatment, name='add_treatment'),
    path('treatments/<int:pk>/edit/', edit_treatment, name='edit_treatment'),
    path('treatments/<int:pk>/delete/', delete_treatment, name='delete_treatment'),

    # Prescriptions
    path('prescriptions/', prescriptions, name='prescriptions'),
    path('prescriptions/add/', add_prescription, name='add_prescription'),
    path('prescriptions/<int:pk>/edit/', edit_prescription, name='edit_prescription'),
    path('prescriptions/<int:pk>/delete/', delete_prescription, name='delete_prescription'),

    # Patient bills
    path('bills/', bills, name='bills'),
    path('bills/add/', add_bill, name='add_bill'),
    path('bills/<int:pk>/edit/', edit_bill, name='edit_bill'),
    path('bills/<int:pk>/delete/', delete_bill, name='delete_bill'),

    # Payments
    path('payments/', payments, name='payments'),
    path('payments/add/', add_payment, name='add_payment'),
    path('payments/<int:pk>/edit/', edit_payment, name='edit_payment'),
    path('payments/<int:pk>/delete/', delete_payment, name='delete_payment'),
]
