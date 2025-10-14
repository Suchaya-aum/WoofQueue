# forms.py
import datetime
from django import forms
from django.db.models import Q
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'service', 'appointment_time', 'finish_time', 'status']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local', "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",}),
            'finish_time': forms.DateTimeInput(attrs={'type': 'datetime-local', "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500", "readonly": "readonly"}),
            'service' : forms.SelectMultiple(attrs={'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400'}),
            "pet": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            "status": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time < timezone.now():
            raise forms.ValidationError("Appointment time cannot be in the past")
        return appointment_time

<<<<<<< Updated upstream
class AppointmentBookingForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'service', 'appointment_time', 'finish_time']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'finish_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'readonly': 'readonly',
            }),
            'service': forms.SelectMultiple(attrs={
                'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400',
            }),
            'pet': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            }),
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time < timezone.now():
            raise forms.ValidationError("Appointment time cannot be in the past")
        return appointment_time

=======
>>>>>>> Stashed changes
class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['size', 'hair_type', 'pet_name', 'behavior_note']
        widgets = {
            "owner": forms.Select(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
            "size": forms.Select(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
            "้hair_type": forms.Select(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
            "pet_name": forms.TextInput(
                attrs={
                    "class": 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'placeholder': 'Enter your pet name'
                }),
            "behavior_note": forms.Textarea(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    'rows': 3,
                    'placeholder': 'Describe your pet’s behavior (e.g. friendly, calm, normal)'
                }),
        }
    def clean_size(self):
        size = self.cleaned_data.get('size')
        if not size:
            raise forms.ValidationError("Pet size is required.")
        return size

    def clean_hair_type(self):
        hair_type = self.cleaned_data.get('hair_type')
        if not hair_type:
            raise forms.ValidationError("Pet hair type is required.")
        return hair_type

    def clean_pet_name(self):
        name = self.cleaned_data.get('pet_name')
        if not name:
            raise forms.ValidationError("Pet name is required.")
        return name

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get("pet_name")
        owner = getattr(self, "owner", None)
        if owner and name:
            qs = Pet.objects.filter(owner=owner, pet_name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error("pet_name", "You already have a pet with this name.")
        return cleaned

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
<<<<<<< Updated upstream
        fields = ["first_name", "last_name", "phone"]
=======
        fields = "__all__"
>>>>>>> Stashed changes
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "p-2 border border-gray-300 rounded-md w-full",
                "placeholder": "Enter first name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "p-2 border border-gray-300 rounded-md w-full",
                "placeholder": "Enter last name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "p-2 border border-gray-300 rounded-md w-full",
                "placeholder": "Enter phone number"
<<<<<<< Updated upstream
=======
            }),
            "user": forms.Select(attrs={
                "class": "p-2 border border-gray-300 rounded-md w-full"
>>>>>>> Stashed changes
            })
        }
        def clean_phone(self):
            phone = self.cleaned_data.get("phone")
            if phone:
                if not phone.isdigit():
                    raise ValidationError("Phone number must contain only digits.")
                if len(phone) != 10:
                    raise ValidationError("Phone number must be exactly 10 digits.")
            return phone

        def clean(self):
            cleaned = super().clean()
            first = cleaned.get("first_name")
            last = cleaned.get("last_name")
            if not first or not last:
                raise ValidationError("Please fill both first name and last name.")
            return cleaned