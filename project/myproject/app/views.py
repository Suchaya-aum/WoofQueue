from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F, Count, Value
from django.db.models.functions import Concat
from app.models import *
from app.forms import *
from django.db import transaction

class AppointmentCreateView(View):

    def get(self, request):
        appointmentForm = AppointmentForm()
        return render(request, "create_appointment.html", {"appointmentform": appointmentForm})
    
    def post(self, request):
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save()
            
            appointment.save()
            return redirect("appointment")
        return render(request, "create_appointment.html", {"appointmentform": appointmentForm})
    
class ServiceCreateView(View):

    def get(self, request):
        serviceform = ServiceForm()
        return render(request, "create_service.html", {"serviceform": serviceform})
    
    def post(self, request):
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            new_service = serviceform.save()
            
            new_service.save()
            return redirect("service")
        return render(request, "create_service.html", {"serviceform": serviceform})
    
class ServiceUpdateView(View):

    def get(self, request, pk):
        service = Service.objects.get(pk=pk)
        serviceform = ServiceForm(instance=service)
        return render(request, "update_service.html", {"serviceform": serviceform, "id": pk})
    
    def post(self, request, pk):
        print("test")
        service = Service.objects.get(pk=pk)
        serviceform = ServiceForm(request.POST, instance=service)
        if serviceform.is_valid():
            new_service = serviceform.save()
            
            return redirect("service")
        print(serviceform.errors)
        print("Test")
        return render(request, "update_service.html", {"serviceform": serviceform, "id": pk})


class ServiceManagementView(View):
    def get(self, request):
        service_list = Service.objects.all()
        print(service_list[0].staff_id.staff_profile.first_name)
        return render(request, "service.html", {"service_list": service_list})