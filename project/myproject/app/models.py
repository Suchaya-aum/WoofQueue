from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)

class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, null=True, blank=True)
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
    owner = models.ForeignKey(Customer, null=False)
    size = models.ForeignKey(Size, null=False)
    hair_type = models.ForeignKey(HairType, null=False)
    pet_name = models.CharField(max_length=25, null=False)
    behavior_note = models.CharField(null=True)
