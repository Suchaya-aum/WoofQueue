from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
# class Customer(models.Model):
#     username = models.CharField(max_length=50, null=False)
#     password = models.CharField(max_length=50, null=False)
#     email = models.EmailField(null=False)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11, null=True, blank=True)

class Size(models.Model):
    class SizeChoices(models.TextChoices):
        S   = "S",   "S"
        M   = "M",   "M"
        L   = "L",   "L"
        XL  = "XL",  "XL"
        XXL = "XXL", "XXL"

    size = models.CharField(max_length=5, choices=SizeChoices.choices, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.size} - {self.price}"
class HairType(models.Model):
    class HairChoices(models.TextChoices):
        LONG_HAIR = "Long Hair", "Long Hair"
        HAIR_BORN = "Hair Born", "Hair Born"
        NORMAL = "Normal", "Normal"

    hair = models.CharField(max_length=20, choices=HairChoices.choices, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.hair} - {self.price}"
class Pet(models.Model):
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
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
    finish_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=Status_Choices, null=False)
    service = models.ManyToManyField("Service")

    def __str__(self):
        return f"PET_ID : {self.pet_id} - APPOINTMENT DATE : {self.appointment_time:%Y-%m-%d %H:%M}"

class Invoice(models.Model):
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Invoice for Appointment {self.appointment_id.id} - Total: ${self.total_price}"

class Service(models.Model):
    service_name = models.CharField(max_length=50, null=False)
    duration = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")

    def __str__(self):
        return f"Service {self.service_name} - {self.duration} minutes - ${self.price} -Staff ID: {self.staff}"

# class Staff(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.CharField(max_length=150)

#     def __str__(self):
#         return f"Staff {self.username}"

class Staff_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=11, null=False)

    def __str__(self):
        return f"{self.user.id} Staff Profile {self.first_name} {self.last_name} - Phone: {self.phone}"
