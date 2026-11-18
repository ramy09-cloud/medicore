from django.contrib import admin
from .models import Patient, Doctor, Diagnosis, PatientBill, Payment, Prescription, Treatment, Appointment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_id", "name", "gender", "age", "contact", "address")
    search_fields = ("name", "contact")
    list_filter = ("gender",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("doctor_id", "first_name", "last_name", "designation", "gender", "contact")
    search_fields = ("first_name", "last_name")
    list_filter = ("designation", "gender")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_id", "date", "time", "patient", "doctor", "status")
    list_filter = ("status", "date", "doctor")
    search_fields = ("patient__name", "reason")
    date_hierarchy = "date"


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    readonly_fields = ("amount",)


class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 0


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ("diagnosis_id", "date", "patient", "doctor")
    list_filter = ("date", "doctor")
    search_fields = ("patient__name", "description")
    inlines = [TreatmentInline, PrescriptionInline]


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(PatientBill)
class PatientBillAdmin(admin.ModelAdmin):
    list_display = ("bill_id", "patient", "total_amount", "total_amount_paid", "balance", "status")
    list_filter = ("status",)
    readonly_fields = ("total_amount_paid", "balance", "status")
    search_fields = ("patient__name",)
    inlines = [PaymentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.save()  # recalc balance after inline payments


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("payment_id", "date", "bill", "amount_paid", "mode_of_payment")
    list_filter = ("mode_of_payment", "date")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("prescription_id", "diagnosis", "medicine", "qty", "price", "amount")
    search_fields = ("medicine",)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("treatment_id", "diagnosis", "price", "status")
    list_filter = ("status",)
