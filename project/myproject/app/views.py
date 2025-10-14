# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import F, Count, Value, Sum
from django.db.models.functions import Concat, TruncDate
from datetime import datetime, timedelta
from app.models import *
from app.forms import *
from authen.forms import SignUpForm
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
<<<<<<< Updated upstream
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
=======
    ALLOWED_STATUS = [
        # (Appointment.Status.LATE, Appointment.Status.LATE.label),
        # (Appointment.Status.CANCELLED, Appointment.Status.CANCELLED.label),
        (Appointment.Status_Choices.BOOKED, Appointment.Status_Choices.BOOKED.label),
    ]
    def _limit_status_choices(self, form):
        # บังคับให้ฟอร์มแสดงเฉพาะ 3 ตัวเลือกนี้ และ validate ตามนี้ด้วย
        form.fields['status'].choices = self.ALLOWED_STATUS
        form.fields['status'].widget.choices = self.ALLOWED_STATUS

    def get(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        pets = Pet.objects.filter(owner=profile)
        form = AppointmentForm()
        form.fields['pet'].queryset = pets
        form.fields['service'].queryset = Service.objects.all()
        self._limit_status_choices(form) # จำกัดสถานะตอนแสดงฟอร์ม
        return render(request, 'create_booking.html', {'booking_form': form, 'pet_exist': pets.exists()})

    def post(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        pets = Pet.objects.filter(owner=profile)
        form = AppointmentForm(request.POST)
        form.fields['pet'].queryset = pets
        form.fields['service'].queryset = Service.objects.all()
        self._limit_status_choices(form)  # จำกัดสถานะซ้ำตอน POST (กันส่งค่าปลอม)


        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            form.save_m2m()

            if appointment.appointment_time:
                total = appointment.service.aggregate(total_time=Sum('duration'))['total_time'] or 0
                appointment.finish_time = appointment.appointment_time + timedelta(minutes=total)
                appointment.save(update_fields=['finish_time'])

            return redirect('appointment')

        return render(request, 'create_booking.html', {'booking_form': form, 'pet_exist': pets.exists()})
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
class BookingUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = Appointment.Status_Choices.LATE
        appointment.save(update_fields=["status"])

        return redirect("appointment")

class AppointmentUpdateView (LoginRequiredMixin, View):
=======
class AppointmentUpdateView(LoginRequiredMixin, View):
    ALLOWED_STATUS = [
        (Appointment.Status_Choices.LATE, Appointment.Status_Choices.LATE.label),
        (Appointment.Status_Choices.CANCELLED, Appointment.Status_Choices.CANCELLED.label),
        (Appointment.Status_Choices.BOOKED, Appointment.Status_Choices.BOOKED.label),
    ]
    def _limit_status_choices(self, form):
        # บังคับให้ฟอร์มแสดงเฉพาะ 3 ตัวเลือกนี้ และ validate ตามนี้ด้วย
        form.fields['status'].choices = self.ALLOWED_STATUS
        form.fields['status'].widget.choices = self.ALLOWED_STATUS

>>>>>>> Stashed changes
    def get(self, request, pk):
        # ดึงข้อมูลนัดหมายที่จะแก้ไข
        appointment = get_object_or_404(Appointment, pk=pk)
        # ฟอร์มแสดงข้อมูลเก่า
        form = AppointmentForm(instance=appointment)
        self._limit_status_choices(form) # จำกัดสถานะตอนแสดงฟอร์ม
        if "service" in form.fields:
            form.fields["service"].queryset = Service.objects.all()

        return render(request,"update_appointment.html",{"appointmentform": form, "id": pk})

    def post(self, request, pk):
        # ดึงข้อมูลนัดหมายที่จะแก้ไข
        appointment = get_object_or_404(Appointment, pk=pk)
        # สร้างฟอร์มจาก POST + instance เดิม
        form = AppointmentForm(request.POST, instance=appointment)
        self._limit_status_choices(form)  # จำกัดสถานะซ้ำตอน POST (กันส่งค่าปลอม)

        # ตั้ง queryset ให้ฟิลด์ service อีกครั้งใน POST
        if "service" in form.fields:
            form.fields["service"].queryset = Service.objects.all()

        if form.is_valid():
            # บันทึกข้อมูลเบื้องต้นก่อน (ยังไม่ commit ลง DB)
            updated = form.save(commit=False)
<<<<<<< Updated upstream
            updated.save()
=======

            # คำนวณ finish_time ใหม่จาก service ที่เลือก
            services = form.cleaned_data.get("service")
            appointment_time = form.cleaned_data.get("appointment_time") or updated.appointment_time

            if services and appointment_time:
                total_duration = services.aggregate(total_time=Sum("duration"))["total_time"] or 0
                updated.finish_time = appointment_time + timedelta(minutes=total_duration)
            # ถ้าไม่มี service เลือก หรือไม่มีเวลาเริ่ม จะไม่เปลี่ยน finish_time เดิม

            # บันทึกลงฐานข้อมูล
            updated.save()
            # บันทึกข้อมูล ManyToMany (service)
>>>>>>> Stashed changes
            form.save_m2m()
            return redirect("appointment")
        return render(request,"update_appointment.html",{"appointmentform": form, "id": pk})

class AppointmentDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, "confirm_delete_appointment.html", {"appointment": appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect("appointment")

<<<<<<< Updated upstream
class CustomerProfileUpdateView(LoginRequiredMixin, View):
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

class PetUpdateView(LoginRequiredMixin, View):
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

class ManageCustomerView(LoginRequiredMixin, View):
    # def test_func(self):
    #     return self.request.user.is_staff

    def get(self, request):
        customers = CustomerProfile.objects.select_related("user").all().order_by("id")
        pets = Pet.objects.select_related("owner").all().order_by("id")

        return render(request, "manage_customer.html", {
            "customers": customers,
            "pets": pets,
        })
=======
# class ManageCustomerView(LoginRequiredMixin, View):
#     def get(self, request):
#         # ดึงข้อมูลลูกค้าทั้งหมด
#         customers = CustomerProfile.objects.select_related("user").all().order_by("id")
#         return render(request, "manage_customer.html", {
#             "customers": customers,
#             "c_form": SignUpForm(),         # ฟอร์ม user
#             "p_form": CustomerProfileForm() # ฟอร์มโปรไฟล์
#         })

#     @transaction.atomic
#     def post(self, request):
#         c_form = SignUpForm(request.POST)
#         p_form = CustomerProfileForm(request.POST)

#         if c_form.is_valid() and p_form.is_valid():
#             # 1. บันทึก User
#             user = c_form.save()

#             # 2. บันทึก CustomerProfile ผูกกับ User
#             profile = p_form.save(commit=False)
#             profile.user = user
#             profile.save()

#             # กลับมาหน้า manage_customer
#             return redirect("manage_customer")

#         # ถ้าไม่ผ่าน validation ส่งกลับหน้าเดิมพร้อม error
#         customers = CustomerProfile.objects.select_related("user").all().order_by("id")
#         return render(request, "manage_customer.html", {
#             "customers": customers,
#             "c_form": c_form,
#             "p_form": p_form
#         })

# class CustomerDeleteView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         customer = get_object_or_404(CustomerProfile, pk=pk)
#         if customer.user:
#             customer.user.delete()
#         customer.delete()
#         return redirect("manage_customer")
>>>>>>> Stashed changes
