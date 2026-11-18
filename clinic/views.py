from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm

from .forms import (AppointmentForm, DiagnosisForm, DoctorForm, PatientBillForm, PatientForm,
                    PaymentForm, PrescriptionForm, TreatmentForm)
from .models import (Appointment, Diagnosis, Doctor, Patient, PatientBill, Payment, Prescription,
                     Treatment)


# ---------------------------------------------------------------
# Helpers shared by every page (list, add/edit, delete)
# ---------------------------------------------------------------
def show_list(request, model, template, search_fields):
    """List page with a search box."""
    items = model.objects.all().order_by("-pk")
    q = request.GET.get("q", "").strip()
    if q:
        condition = Q()
        for field in search_fields:
            condition |= Q(**{f"{field}__icontains": q})
        items = items.filter(condition)
    return render(request, template, {"items": items, "q": q})


def show_form(request, form_class, template, list_page, model=None, pk=None):
    """Add page (no pk) or Edit page (with pk)."""
    obj = get_object_or_404(model, pk=pk) if pk else None
    form = form_class(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Saved successfully.")
        return redirect(list_page)
    return render(request, template, {"form": form, "obj": obj})


def delete_record(request, model, pk, list_page):
    """Asks 'Are you sure?' then deletes."""
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, "Deleted successfully.")
        except ProtectedError:
            messages.error(request, "Can't delete: other records depend on it.")
        return redirect(list_page)
    return render(request, "confirm_delete.html", {"obj": obj, "list_page": list_page})


# ---------------------------------------------------------------
# Home / dashboard
# ---------------------------------------------------------------
@login_required
def index(request):
    context = {
        "patients": Patient.objects.count(),
        "doctors": Doctor.objects.count(),
        "appointments": Appointment.objects.count(),
        "diagnoses": Diagnosis.objects.count(),
        "treatments": Treatment.objects.count(),
        "prescriptions": Prescription.objects.count(),
        "bills": PatientBill.objects.count(),
        "payments": Payment.objects.count(),
        "revenue": Payment.objects.aggregate(s=Sum("amount_paid"))["s"] or 0,
        "outstanding": PatientBill.objects.aggregate(s=Sum("balance"))["s"] or 0,
        "recent": Diagnosis.objects.select_related("patient", "doctor").order_by("-date")[:5],
        "upcoming": Appointment.objects.select_related("patient", "doctor")
                                       .filter(status="Scheduled").order_by("date", "time")[:5],
    }
    return render(request, "index.html", context)


# ---------------------------------------------------------------
# Patients
# ---------------------------------------------------------------
@login_required
def patients(request):
    return show_list(request, Patient, "patients.html", ["name", "contact", "address"])


@login_required
def add_patient(request):
    return show_form(request, PatientForm, "patient_form.html", "patients")


@login_required
def edit_patient(request, pk):
    return show_form(request, PatientForm, "patient_form.html", "patients", Patient, pk)


@login_required
def delete_patient(request, pk):
    return delete_record(request, Patient, pk, "patients")


# ---------------------------------------------------------------
# Doctors
# ---------------------------------------------------------------
@login_required
def doctors(request):
    return show_list(request, Doctor, "doctors.html", ["first_name", "last_name", "designation", "contact"])


@login_required
def add_doctor(request):
    return show_form(request, DoctorForm, "doctor_form.html", "doctors")


@login_required
def edit_doctor(request, pk):
    return show_form(request, DoctorForm, "doctor_form.html", "doctors", Doctor, pk)


@login_required
def delete_doctor(request, pk):
    return delete_record(request, Doctor, pk, "doctors")


# ---------------------------------------------------------------
# Appointments
# ---------------------------------------------------------------
@login_required
def appointments(request):
    return show_list(request, Appointment, "appointments.html", ["patient__name", "reason", "status"])


@login_required
def add_appointment(request):
    return show_form(request, AppointmentForm, "appointment_form.html", "appointments")


@login_required
def edit_appointment(request, pk):
    return show_form(request, AppointmentForm, "appointment_form.html", "appointments", Appointment, pk)


@login_required
def delete_appointment(request, pk):
    return delete_record(request, Appointment, pk, "appointments")


# ---------------------------------------------------------------
# Diagnoses
# ---------------------------------------------------------------
@login_required
def diagnoses(request):
    return show_list(request, Diagnosis, "diagnoses.html", ["patient__name", "description"])


@login_required
def add_diagnosis(request):
    return show_form(request, DiagnosisForm, "diagnosis_form.html", "diagnoses")


@login_required
def edit_diagnosis(request, pk):
    return show_form(request, DiagnosisForm, "diagnosis_form.html", "diagnoses", Diagnosis, pk)


@login_required
def delete_diagnosis(request, pk):
    return delete_record(request, Diagnosis, pk, "diagnoses")


# ---------------------------------------------------------------
# Treatments
# ---------------------------------------------------------------
@login_required
def treatments(request):
    return show_list(request, Treatment, "treatments.html", ["description", "status"])


@login_required
def add_treatment(request):
    return show_form(request, TreatmentForm, "treatment_form.html", "treatments")


@login_required
def edit_treatment(request, pk):
    return show_form(request, TreatmentForm, "treatment_form.html", "treatments", Treatment, pk)


@login_required
def delete_treatment(request, pk):
    return delete_record(request, Treatment, pk, "treatments")


# ---------------------------------------------------------------
# Prescriptions
# ---------------------------------------------------------------
@login_required
def prescriptions(request):
    return show_list(request, Prescription, "prescriptions.html", ["medicine", "time_taken"])


@login_required
def add_prescription(request):
    return show_form(request, PrescriptionForm, "prescription_form.html", "prescriptions")


@login_required
def edit_prescription(request, pk):
    return show_form(request, PrescriptionForm, "prescription_form.html", "prescriptions", Prescription, pk)


@login_required
def delete_prescription(request, pk):
    return delete_record(request, Prescription, pk, "prescriptions")


# ---------------------------------------------------------------
# Patient bills
# ---------------------------------------------------------------
@login_required
def bills(request):
    return show_list(request, PatientBill, "bills.html", ["patient__name", "status"])


@login_required
def add_bill(request):
    return show_form(request, PatientBillForm, "bill_form.html", "bills")


@login_required
def edit_bill(request, pk):
    return show_form(request, PatientBillForm, "bill_form.html", "bills", PatientBill, pk)


@login_required
def delete_bill(request, pk):
    return delete_record(request, PatientBill, pk, "bills")


# ---------------------------------------------------------------
# Payments
# ---------------------------------------------------------------
@login_required
def payments(request):
    return show_list(request, Payment, "payments.html", ["mode_of_payment", "bill__patient__name"])


@login_required
def add_payment(request):
    return show_form(request, PaymentForm, "payment_form.html", "payments")


@login_required
def edit_payment(request, pk):
    return show_form(request, PaymentForm, "payment_form.html", "payments", Payment, pk)


@login_required
def delete_payment(request, pk):
    return delete_record(request, Payment, pk, "payments")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
