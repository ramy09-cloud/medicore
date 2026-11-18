from django import forms

from .models import Patient, Doctor, Appointment, Diagnosis, Treatment, Prescription, PatientBill, Payment

# Date and time pickers for the browser
DATE = forms.DateInput(attrs={"type": "date"})
TIME = forms.TimeInput(attrs={"type": "time"})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {"date_of_birth": DATE}


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {"date": DATE, "time": TIME}


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = "__all__"
        widgets = {"date": DATE, "description": forms.Textarea(attrs={"rows": 3})}


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = "__all__"
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = "__all__"   # "amount" is worked out automatically (qty x price)


class PatientBillForm(forms.ModelForm):
    class Meta:
        model = PatientBill
        fields = "__all__"   # paid, balance and status are worked out automatically


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {"date": DATE}
