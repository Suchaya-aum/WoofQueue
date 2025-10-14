import datetime
from django import forms
from django.db.models import Q
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            "appointment_time": forms.DateTimeInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "datetime-local"
                }
            ),
            "finish_time": forms.DateTimeInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "datetime-local",
                    "readonly": "readonly"
                }
            ),
            "service": forms.SelectMultiple(
                attrs={
                    'class': 'block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
                }
            ),
            "pet_id": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            "status": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        }

    def clean(self):
        cleaned_data = super().clean()

        appoint_time = cleaned_data.get("appointment_time")
        fin_time = cleaned_data.get("finish_time")


        for s in cleaned_data.get("service"):
            if Appointment.objects.filter(appointment_time__gte=appoint_time, appointment_time__lte=fin_time, service = s):
                self.add_error("finish_time", "Finish time is overlap with other appointment")
            elif Appointment.objects.filter(finish_time__range=(appoint_time, fin_time), service = s):
                self.add_error("appointment_time", "There is other appointment at this time.")
        #     self.add_error("appointment_time", "This time of the day has booked")
        return cleaned_data
    
class AppointmentStaffForm(ModelForm):

    pet_id = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            "appointment_time": forms.DateTimeInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "datetime-local"
                }
            ),
            "finish_time": forms.DateTimeInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "type": "datetime-local",
                    "readonly": "readonly"
                }
            ),
            "service": forms.SelectMultiple(
                attrs={
                    'class': 'block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
                }
            ),
            "pet_id": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            "status": forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
        }

    def clean(self):
        cleaned_data = super().clean()

        appoint_time = cleaned_data.get("appointment_time")
        fin_time = cleaned_data.get("finish_time")


        for s in cleaned_data.get("service"):
            if Appointment.objects.filter(appointment_time__gte=appoint_time, appointment_time__lte=fin_time, service = s):
                self.add_error("finish_time", "Finish time is overlap with other appointment")
            elif Appointment.objects.filter(finish_time__range=(appoint_time, fin_time), service = s):
                self.add_error("appointment_time", "There is other appointment at this time.")
        #     self.add_error("appointment_time", "This time of the day has booked")
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
        widgets = {
            "service_name": forms.TextInput(
                attrs={
                    "class": 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                }),
            "duration": forms.TextInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
            "price": forms.NumberInput(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
            "staff": forms.Select(
                attrs={
                    "class": "p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }),
        }

