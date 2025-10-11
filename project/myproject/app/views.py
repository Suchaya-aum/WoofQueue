from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F, Count, Value
from django.db.models.functions import Concat
from app.models import *
from app.forms import *
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ServiceCreateView(View):

    def get(self, request):
        serviceform = ServiceForm()
        return render(request, "create_service.html", {"serviceform": serviceform})
    
    def post(self, request):
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            new_service = serviceform.save()
            
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
        return render(request, "service.html", {"service_list": service_list})
    
class InvoiceView(View):
    def get(self, request):
        invoice_list = Service.objects.all()
        return render(request, "invoice.html", {"invoice_list": invoice_list})

# ✅ ลูกค้าและพนักงานเห็นรายการนัดได้ (แต่ filter ต่างกัน)
class AppointmentView(LoginRequiredMixin, View):
    # permission_required = 'appointments.view_appointment'
    # raise_exception = True  # ถ้าไม่มีสิทธิ์ → 403

    def get(self, request):
        # JOIN pet และ owner เพื่อลด query ซ้ำ
        # ใช้ query set
        qs = (
            Appointment.objects
            .select_related('pet_id', 'pet_id__owner')  # ใช้ pet_id ให้ตรงชื่อฟิลด์
            .prefetch_related('service')                # M2M ชื่อ service (เอกพจน์)
            .order_by('-id')
        )

        return render(request, 'appointment.html', {'appointments': qs})


class BookingCreateView(LoginRequiredMixin, View):  
    def get(self, request):
        booking_form = AppointmentForm()
        return render(request, "create_booking.html", {"booking_form": booking_form})
    
    def post(self, request):
        booking_form = AppointmentForm(request.POST)
        if booking_form.is_valid():
            appointment = booking_form.save()
            
            appointment.save()
            return redirect("appointment")
        return render(request, "create_booking.html", {"booking_form": booking_form})


class AppointmentCreateView(LoginRequiredMixin, View):
    # permission_required = 'appointments.add_appointment'
    raise_exception = True

    def get(self, request):
        form = AppointmentForm()
        return render(request, "create_appointment.html", {"appointmentform": form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.save()
            form.save_m2m()
            return redirect("appointment")
        return render(request, "create_appointment.html", {"appointmentform": form})


# ✅ ลูกค้าและพนักงานเห็นรายการนัดได้ (แต่ filter ต่างกัน)
class AppointmentView(LoginRequiredMixin, View):
    # permission_required = 'appointments.view_appointment'
    # raise_exception = True  # ถ้าไม่มีสิทธิ์ → 403

    def get(self, request):
        # JOIN pet และ owner เพื่อลด query ซ้ำ
        # ใช้ query set
        qs = (
            Appointment.objects
            .select_related('pet_id', 'pet_id__owner')  # ใช้ pet_id ให้ตรงชื่อฟิลด์
            .prefetch_related('service')                # M2M ชื่อ service (เอกพจน์)
            .order_by('-id')
        )

        return render(request, 'appointment.html', {'appointments': qs})


class BookingCreateView(LoginRequiredMixin, View):  
    def get(self, request):
        booking_form = AppointmentForm()
        return render(request, "create_booking.html", {"booking_form": booking_form})
    
    def post(self, request):
        booking_form = AppointmentForm(request.POST)
        if booking_form.is_valid():
            appointment = booking_form.save()
            
            appointment.save()
            return redirect("appointment")
        return render(request, "create_booking.html", {"booking_form": booking_form})


class AppointmentCreateView(LoginRequiredMixin, View):
    # permission_required = 'appointments.add_appointment'
    raise_exception = True

    def get(self, request):
        form = AppointmentForm()
        return render(request, "create_appointment.html", {"appointmentform": form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.save()
            form.save_m2m()
            return redirect("appointment")
        return render(request, "create_appointment.html", {"appointmentform": form})
