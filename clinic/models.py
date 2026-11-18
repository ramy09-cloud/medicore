from django.db import models


class Patient(models.Model):
    GENDER = [("Male", "Male"), ("Female", "Female")]
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER)
    age = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=1, help_text="kg")
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER = [("Male", "Male"), ("Female", "Female")]
    DESIGNATION = [("Doctor", "Doctor"), ("Nurse", "Nurse")]
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    gender = models.CharField(max_length=10, choices=GENDER)
    designation = models.CharField(max_length=20, choices=DESIGNATION)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.designation} {self.first_name} {self.last_name}"


class Diagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "diagnoses"

    def __str__(self):
        return f"#{self.diagnosis_id} {self.patient} ({self.date})"


class PatientBill(models.Model):
    STATUS = [("Unpaid", "Unpaid"), ("Partial", "Partial"), ("Paid", "Paid")]
    bill_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=10, choices=STATUS, default="Unpaid", editable=False)

    def recalc(self):
        paid = sum(p.amount_paid for p in self.payment_set.all())
        self.total_amount_paid = paid
        self.balance = self.total_amount - paid
        self.status = "Paid" if self.balance <= 0 and self.total_amount > 0 else ("Partial" if paid > 0 else "Unpaid")

    def save(self, *args, **kwargs):
        if self.pk:
            self.recalc()
        else:
            self.balance = self.total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.bill_id} - {self.patient}"


class Payment(models.Model):
    MODES = [("Cash", "Cash"), ("Mobile Money", "Mobile Money"), ("Card", "Card"), ("Insurance", "Insurance")]
    payment_id = models.AutoField(primary_key=True)
    date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    mode_of_payment = models.CharField(max_length=20, choices=MODES)
    bill = models.ForeignKey(PatientBill, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bill.save()  # update balance/status

    def delete(self, *args, **kwargs):
        bill = self.bill
        super().delete(*args, **kwargs)
        bill.save()

    def __str__(self):
        return f"Payment #{self.payment_id}"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=150)
    qty = models.PositiveIntegerField()
    time_taken = models.CharField(max_length=100, help_text="e.g. 2x daily after meals")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.amount = self.qty * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine} x{self.qty}"


class Treatment(models.Model):
    STATUS = [("Pending", "Pending"), ("Ongoing", "Ongoing"), ("Completed", "Completed")]
    treatment_id = models.AutoField(primary_key=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")

    def __str__(self):
        return f"Treatment #{self.treatment_id}"


class Appointment(models.Model):
    STATUS = [("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Cancelled", "Cancelled")]
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default="Scheduled")

    def __str__(self):
        return f"Appt #{self.appointment_id} {self.patient} - {self.date}"
