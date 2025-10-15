# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import F, Count, Value, Sum
from django.db.models.functions import Concat, TruncDate
from datetime import datetime, timedelta
from app.models import *
from app.forms import *
from authen.forms import *
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json
from .utils import get_plot

class DashboardView(PermissionRequiredMixin, View):
    permission_required = ["app.view_invoice"]

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


class ServiceCreateView(PermissionRequiredMixin, View):
    permission_required = ["app.add_service"]

    def get(self, request):
        serviceform = ServiceForm()
        return render(request, "create_service.html", {"serviceform": serviceform})
    
    def post(self, request):
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            new_service = serviceform.save()
            
            return redirect("service")
        return render(request, "create_service.html", {"serviceform": serviceform})
    
class ServiceUpdateView(PermissionRequiredMixin, View):
    permission_required = ["app.change_service"]

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


class ServiceManagementView(PermissionRequiredMixin, View):
    permission_required = ["app.view_service"]

    def get(self, request):
        service_list = Service.objects.all()
        return render(request, "service.html", {"service_list": service_list})
    
class InvoiceView(PermissionRequiredMixin, View):
    permission_required = ["app.view_invoice"]

    def get(self, request):
        invoice_list = Invoice.objects.all()
        return render(request, "invoice.html", {"invoice_list": invoice_list})

# ลูกค้าและพนักงานเห็นรายการนัดได้ (แต่ filter ต่างกัน)
class AppointmentView(PermissionRequiredMixin, View):
    permission_required = ["app.view_appointment"]
    # raise_exception = True  # ถ้าไม่มีสิทธิ์ → 403

    def get(self, request):
        # JOIN pet และ owner เพื่อลด query ซ้ำ
        # ใช้ query set
        qs = (
            Appointment.objects
            .select_related('pet', 'pet__owner', 'pet__owner__user')
            .prefetch_related('service')
            .order_by('-id')
            .filter(~Q(status="PU"))
        )


        return render(request, 'appointment.html', {'appointments': qs})


class BookingCreateView(PermissionRequiredMixin, View):
    permission_required = ["app.add_appointment"]

    def get(self, request):
        # ดึง profile ของ user ที่ล็อกอินอยู่
        profile = get_object_or_404(CustomerProfile, user=request.user)
        # pet ที่เป็นของ user นี้
        pets = Pet.objects.filter(owner=profile)
        form = AppointmentBookingForm()
        form.fields['pet'].queryset = pets
        form.fields['service'].queryset = Service.objects.all()
        service_list = Service.objects.all()

        return render(request, 'create_booking.html', {
            'booking_form': form,
            'pet_exist': pets.exists(),
            'service_list': service_list
        })

    def post(self, request):
        # ดึงข้อมูล customer profile
        profile = get_object_or_404(CustomerProfile, user=request.user)

        form = AppointmentBookingForm(request.POST)
        form.fields['pet'].queryset = Pet.objects.filter(owner=profile)
        form.fields['service'].queryset = Service.objects.all()

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = Appointment.Status_Choices.BOOKED
            appointment.save()
            form.save_m2m()

            total_time = appointment.service.aggregate(total_time=Sum("duration"))
            appointment.finish_time = appointment.appointment_time + timedelta(minutes=total_time["total_time"])
            appointment.save(update_fields=['finish_time'])

            return redirect('appointment')
        return render(request, 'create_booking.html', {
            'booking_form': form,
            'pet_exist': True,
        })

class AppointmentCreateView(PermissionRequiredMixin, View):
    permission_required = ['app.add_appointment', 'app.view_invoice']

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


class PetCreateView(PermissionRequiredMixin, View):
    permission_required = ['app.add_pet']

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

class BookingUpdateView(PermissionRequiredMixin, View):
    permission_required = ['app.view_appointment']

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = Appointment.Status_Choices.LATE
        appointment.save(update_fields=["status"])

        return redirect("appointment")

# views.py
class AppointmentUpdateView(PermissionRequiredMixin, View):
    permission_required = ['app.change_appointment']

    def get(self, request, pk):
        # ดึงข้อมูลนัดหมายที่จะแก้ไข
        appointment = get_object_or_404(Appointment, pk=pk)
        # ฟอร์มแสดงข้อมูลเก่า
        form = AppointmentUpdateForm(instance=appointment)
        if "service" in form.fields:
            form.fields["service"].queryset = Service.objects.all()

        return render(request,"update_appointment.html",{"appointmentform": form, "id": pk})

    def post(self, request, pk):
        # ดึงข้อมูลนัดหมายที่จะแก้ไข
        appointment = get_object_or_404(Appointment, pk=pk)
        # สร้างฟอร์มจาก POST + instance เดิม
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if "service" in form.fields:
            form.fields["service"].queryset = Service.objects.all()
        if form.is_valid():
            updated = form.save(commit=False)
            services = form.cleaned_data.get("service")
            appointment_time = form.cleaned_data.get("appointment_time") or updated.appointment_time
            if services and appointment_time:
                total_duration = services.aggregate(total_time=Sum("duration"))["total_time"] or 0
                updated.finish_time = appointment_time + timedelta(minutes=total_duration)
            updated.save()
            form.save_m2m()
            if updated.status == "PU":
                invoice = Invoice.objects.create(appointment_id=Appointment.objects.get(pk=pk), total_price=services.aggregate(total_price=Sum("price"))["total_price"])
                invoice.save()

            return redirect("appointment")
        return render(request, "update_appointment.html", {"appointmentform": form, "id": pk})


class AppointmentDeleteView(PermissionRequiredMixin, View):
    permission_required = ['app.delete_appointment']


    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, "confirm_delete_appointment.html", {"appointment": appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect("appointment")

class CustomerProfileUpdateView(PermissionRequiredMixin, View):
    permission_required = ['app.change_customerprofile']


    def get(self, request):
        # ดึงโปรไฟล์ของ user ปัจจุบัน
        profile = get_object_or_404(CustomerProfile, user=request.user)
        form = CustomerProfileForm(instance=profile)
        pets = Pet.objects.filter(owner=profile)  # ดึง pet ทั้งหมดของลูกค้าคนนี้

        return render(request, "customer_profile_edit.html", {
            "form": form,
            "pets": pets, # ส่ง list ของสัตว์เลี้ยง
        })

    def post(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        form = CustomerProfileForm(request.POST, instance=profile)
        pets = Pet.objects.filter(owner=profile)

        if form.is_valid():
            form.save()
            return redirect("appointment")

        return render(request, "customer_profile_edit.html", {
            "form": form,
            "pets": pets,
            "pet_exist": pets.exists(),
        })

class PetUpdateView(PermissionRequiredMixin, View):
    permission_required = ['app.change_pet']


    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk, owner__user=request.user)
        form = PetForm(instance=pet)
        return render(request, "pet_edit.html", {"form": form, "pet": pet})

    def post(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk, owner__user=request.user)
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("pet_edit", pk=pet.pk)
        return render(request, "pet_edit.html", {"form": form, "pet": pet})

class ManageCustomerView(PermissionRequiredMixin, View):
    permission_required = ['app.change_customerprofile', 'app.view_invoice']


    # def test_func(self):
    #     return self.request.user.is_staff

    def get(self, request):
        customers = CustomerProfile.objects.select_related("user").all().order_by("id")
        pets = Pet.objects.select_related("owner").all().order_by("id")

        return render(request, "manage_customer.html", {
            "customers": customers,
            "pets": pets,
        })

    
class NewCustomerView(PermissionRequiredMixin, View):
    permission_required = ['app.add_appointment', 'app.view_invoice']
    raise_exception = True

    def get(self, request):
        customerform = CustomerProfileForm()
        petform = PetForm()
        return render(request, "new_customer.html", {"customerform": customerform, "petform": petform})

    def post(self, request):
        customerform = CustomerProfileForm(request.POST)
        petform = PetForm(request.POST)
        try:
            with transaction.atomic():
                if customerform.is_valid():
                    customerProfile = customerform.save()
                    if petform.is_valid():
                        pet = petform.save(commit=False)
                        pet.owner = customerProfile
                        pet.save()
                        return redirect("appointment_create")
                    return redirect("appointment")
        except Exception as e:
            raise e
        return render(request, "new_customer.html", {"customerform": customerform, "petform": petform})
