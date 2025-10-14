# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import F, Count, Value, Sum
from django.db.models.functions import Concat, TruncDate
from datetime import datetime, timedelta
from app.models import *
from app.forms import *
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json
from .utils import get_plot

class DashboardView(View):
    def get(self, request):
        all_income = []
        appointment_list = Appointment.objects.all().order_by("-appointment_time").filter(appointment_time__date__lt=datetime.datetime.now().date())
        appointment_list_today = Appointment.objects.all().order_by("-appointment_time").filter(appointment_time__date=datetime.datetime.now().date())
        appointment_list_incoming = Appointment.objects.all().order_by("-appointment_time").filter(appointment_time__date__gt=datetime.datetime.now().date())

        dates_list = Appointment.objects.annotate(date_only=TruncDate('appointment_time')).order_by('date_only', 'appointment_time').distinct('date_only').filter(date_only__lte=datetime.datetime.now().date()).values("date_only")
        for d in dates_list:
            income = Appointment.objects.annotate(date_only=TruncDate('appointment_time'), total_income=Sum("service__price")).filter(date_only=d['date_only']).aggregate(total=Sum("total_income"))
            all_income.append(income["total"])

        x = [d["date_only"] for d in dates_list]
        y = [income for income in all_income]
        chart = get_plot(x, y)
        return render(request, "dashboard.html", {"appointment_list": appointment_list, "appointment_list_today": appointment_list_today, "appointment_list_incoming": appointment_list_incoming, "chart": chart})


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

# ลูกค้าและพนักงานเห็นรายการนัดได้ (แต่ filter ต่างกัน)
class AppointmentView(LoginRequiredMixin, View):
    # permission_required = 'appointments.view_appointment'
    # raise_exception = True  # ถ้าไม่มีสิทธิ์ → 403

    def get(self, request):
        # JOIN pet และ owner เพื่อลด query ซ้ำ
        # ใช้ query set
        qs = (
            Appointment.objects
            .select_related('pet', 'pet__owner', 'pet__owner__user')
            .prefetch_related('service')
            .order_by('-id')
        )


        return render(request, 'appointment.html', {'appointments': qs})


class BookingCreateView(LoginRequiredMixin, View):

    def _get_profile_and_pets(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        pets_qs = Pet.objects.filter(owner=profile)
        return profile, pets_qs

    def _apply_service_queryset(self, form):
        # ปรับตามเงื่อนไขของคุณได้ เช่น filter เฉพาะ service ที่ active
        form.fields["service"].queryset = Service.objects.all()

    def get(self, request):
        profile, pets_qs = self._get_profile_and_pets(request)

        booking_form = AppointmentForm()
        booking_form.fields["pet"].queryset = pets_qs
        self._apply_service_queryset(booking_form)

        # รองรับ preselect ?service=1&service=3
        preselect_ids = request.GET.getlist("service")
        if preselect_ids:
            booking_form.initial = booking_form.initial or {}
            booking_form.initial["service"] = preselect_ids

        context = {
            "booking_form": booking_form,
            "pet_exist": pets_qs.exists(),
        }
        return render(request, 'create_booking.html', context)

    def post(self, request):
        profile, pets_qs = self._get_profile_and_pets(request)

        booking_form = AppointmentForm(request.POST)
        booking_form.fields["pet"].queryset = pets_qs
        self._apply_service_queryset(booking_form)

        if booking_form.is_valid():
            # ยืนยันว่า pet เป็นของผู้ใช้
            pet = booking_form.cleaned_data.get("pet")
            if pet is None or pet.owner_id != profile.id:
                booking_form.add_error("pet", "Invalid pet selection.")
            else:
                appointment = booking_form.save(commit=False)

                # คำนวณ finish_time จากผลรวม duration ของ service ที่เลือก
                services = booking_form.cleaned_data.get("service")
                if services and appointment.appointment_time:
                    total = services.aggregate(total_time=Sum("duration"))["total_time"] or 0
                    appointment.finish_time = appointment.appointment_time + timedelta(minutes=total)

                # ถ้าต้องการผูก customer/profile:
                # appointment.customer = profile

                appointment.save()
                booking_form.save_m2m()  # ManyToMany 'service'
                return redirect("appointment")

        if "save_add" in request.POST:
            pet_form = PetForm(request.POST)
            profile = get_object_or_404(CustomerProfile, user=request.user)
            pet_form.owner = profile
            if pet_form.is_valid():
                pet = pet_form.save(commit=False)
                pet.owner = profile
                pet.save()
                return redirect("create_pet")

        context = {
            "booking_form": booking_form,
            "pet_exist": pets_qs.exists(),
        }
        return render(request, 'create_booking.html', context)

class AppointmentCreateView(LoginRequiredMixin, View):
    # permission_required = 'appointments.add_appointment'
    raise_exception = True

    def get(self, request):
        form = AppointmentForm()
        service_list = Service.objects.all()
        return render(request, "create_appointment.html", {"appointmentform": form, "service_list": service_list})

    def post(self, request):
        form = AppointmentForm(request.POST)
        print("Check form")
        if form.is_valid():
            appointment = form.save()
            total_time = appointment.service.aggregate(total_time=Sum("duration"))
            appointment.finish_time = appointment.appointment_time + timedelta(minutes=total_time["total_time"])
            appointment.save()
            return redirect("appointment")
        return render(request, "create_appointment.html", {"appointmentform": form})


class PetCreateView(LoginRequiredMixin, View):
    def get(self, request):
        pet_form = PetForm()
        return render(request, "pet_detail.html", {"pet_form": pet_form})

    def post(self, request):
        pet_form = PetForm(request.POST)
        profile = get_object_or_404(CustomerProfile, user=request.user)
        pet_form.owner = profile
        if pet_form.is_valid():
            pet = pet_form.save(commit=False)
            pet.owner = profile
            pet.save()

            return redirect("booking_request")
        return render(request, "pet_detail.html", {"pet_form": pet_form})

class AppointmentUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = AppointmentForm(instance=appointment)
        return render(request, "update_appointment.html", {"appointmentform": form, "id": pk})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            updated = form.save(commit=False)
            # ตัวอย่าง: ถ้าต้องเก็บคนแก้ไข
            # updated.updated_by = request.user
            updated.save()
            form.save_m2m()  # สำคัญ: เนื่องจากมี ManyToMany 'service'
            return redirect("appointment")
        return render(request, "update_appointment.html", {"appointmentform": form, "id": pk})


class AppointmentDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, "confirm_delete_appointment.html", {"appointment": appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect("appointment")
