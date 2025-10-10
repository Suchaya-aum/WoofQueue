import datetime
from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
