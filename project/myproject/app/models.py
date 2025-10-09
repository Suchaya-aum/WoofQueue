from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)

class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11, null=True, blank=True)

class Size(models.Model):
    class SizeChoices(models.TextChoices):
        S = "S",
        M = "M",
        L = "L",
        XL = "XL",
        XXL = "XXL"

    size = models.CharField(choices=SizeChoices, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class HairType(models.Model):
    class HairChoices(models.TextChoices):
        LongHair = "Long Hair",
        HairBorn = "Hair Born",
        Normal = "Normal"

    hair = models.CharField(choices=HairChoices, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Pet(models.Model):
    owner = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=False, on_delete=models.CASCADE)
    hair_type = models.ForeignKey(HairType, null=False, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=25, null=False)
    behavior_note = models.CharField(max_length=255, null=True)

class Appointment(models.Model):
    class Status_Choices(models.TextChoices):
        BOOKED = "B", _("BOOKED")
        CHECKED_IN = "CI", _("CHECKED_IN")
        IN_PROGRESS = "IP", _("IN_PROGRESS")
        DONE = "D", _("DONE")
        PICKED_UP = "PU", _("PICKED_UP")
        CANCELLED = "C", _("CANCELLED")
        LATE = "L", _("LATE")
    pet_id = models.ForeignKey("Pet", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=Status_Choices, null=False)
    service = models.ManyToManyField("app.Service")

    def __str__(self):
        return f"PET_ID : {self.pet_id} - APPOINTMENT DATE : {self.appointment_date}"

class Invoice(models.Model):
    appointment_id = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(max_length=None, null=True)

    def __str__(self):
        return f"Invoice for Appointment {self.appointment_id} - Total Amount: ${self.total_amount}"

class AppointmentService(models.Model):
    appointment_id = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    service_id = models.ForeignKey("Service", on_delete=models.CASCADE)

class Service(models.Model):
    service_name = models.CharField(max_length=50, null=False)
    duration = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    staff_id = models.ForeignKey("Staff", on_delete=models.CASCADE)

    def __str__(self):
        return f"Service {self.service_name} - {self.duration} minutes - ${self.price} -Staff ID: {self.staff_id}"

class Staff(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=150)

    def __str__(self):
        return f"Staff {self.username} Email: {self.email}"

class Staff_Profile(models.Model):
    staff_id = models.OneToOneField(Staff, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11, null=False)

    def __str__(self):
        return f"ID: {self.staff_id} Staff Profile {self.first_name} {self.last_name} - Phone: {self.phone}"
