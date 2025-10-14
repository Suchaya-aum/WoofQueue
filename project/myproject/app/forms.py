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

    def clean(self):
        cleaned_data = super().clean()
        appoint_time = cleaned_data.get('appointment_time')
        fin_time = cleaned_data.get('finish_time')
        pet = cleaned_data.get('pet')
        # ตรวจเวลาสิ้นสุด
        if fin_time and appoint_time:
            if fin_time and appoint_time and fin_time <= appoint_time:
                raise forms.ValidationError("Finish time must be later than appointment time")
            elif fin_time and appoint_time and (fin_time - appoint_time) > timedelta(hours=8):
                raise forms.ValidationError("Appointment cannot exceed 8 hours duration")
            
            for s in cleaned_data.get("service"):
                if Appointment.objects.filter(appointment_time__gte=appoint_time, appointment_time__lte=fin_time, service = s):
                    self.add_error("finish_time", "Finish time is overlap with other appointment")
                elif Appointment.objects.filter(finish_time__range=(appoint_time, fin_time), service = s):
                    self.add_error("appointment_time", "There is other appointment at this time.")
        # ตรวจเวลาซ้ำในช่วง 1 ชั่วโมง
        if pet and appoint_time:
            # ถ้ามี instance อยู่ (ตอน update) ให้ exclude ตัวเองออกจากการเช็ก
            qs = Appointment.objects.filter(pet=pet)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            # หา appointment ที่อยู่ในช่วงเวลา +- 1 ชั่วโมง ของเวลานี้
            overlap_start = appoint_time - timedelta(hours=1)
            overlap_end = appoint_time + timedelta(hours=1)
            if qs.filter(appointment_time__range=(overlap_start, overlap_end)).exists():
                raise forms.ValidationError(
                    f"This pet already has an appointment within 1 hour of the selected time."
                )

        return cleaned_data

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = "__all__"
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
                }),
            "behavior_note": forms.Textarea(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
        }

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
