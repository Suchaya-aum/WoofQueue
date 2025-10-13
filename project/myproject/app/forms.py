# forms.py
import datetime
from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'service', 'appointment_time', 'finish_time', 'status']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'finish_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'service' : forms.SelectMultiple(attrs={'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400'})
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_time < timezone.now():
            raise forms.ValidationError("Appointment time cannot be in the past")
        return appointment_time

    def clean(self):
        cleaned_data = super().clean()
        appointment_time = cleaned_data.get('appointment_time')
        finish_time = cleaned_data.get('finish_time')
        pet = cleaned_data.get('pet')
        # ตรวจเวลาสิ้นสุด
        if finish_time and appointment_time:
            if finish_time and appointment_time and finish_time <= appointment_time:
                raise forms.ValidationError("Finish time must be later than appointment time")
            elif finish_time and appointment_time and (finish_time - appointment_time) > timedelta(hours=8):
                raise forms.ValidationError("Appointment cannot exceed 8 hours duration")
        # ตรวจเวลาซ้ำในช่วง 1 ชั่วโมง
        if pet and appointment_time:
            # ถ้ามี instance อยู่ (ตอน update) ให้ exclude ตัวเองออกจากการเช็ก
            qs = Appointment.objects.filter(pet=pet)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            # หา appointment ที่อยู่ในช่วงเวลา +- 1 ชั่วโมง ของเวลานี้
            overlap_start = appointment_time - timedelta(hours=1)
            overlap_end = appointment_time + timedelta(hours=1)
            if qs.filter(appointment_time__range=(overlap_start, overlap_end)).exists():
                raise forms.ValidationError(
                    f"This pet already has an appointment within 1 hour of the selected time."
                )

        return cleaned_data

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['size', 'hair_type', 'pet_name', 'behavior_note']
        widgets = {
            'size': forms.Select(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400'
                }
            ),
            'hair_type': forms.Select(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400'
                }
            ),
            'pet_name': forms.TextInput(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400',
                    'placeholder': 'Enter your pet name'
                }
            ),
            'behavior_note': forms.Textarea(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2 focus:ring-2 focus:ring-blue-400',
                    'rows': 3,
                    'placeholder': 'Describe your pet’s behavior (e.g. friendly, calm, normal)'
                }
            ),
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


