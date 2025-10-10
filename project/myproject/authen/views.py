from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

# from django.db.models import Count
# from django.db.models import Value
# from django.db.models.functions import Concat

from .models import *
from django.core.exceptions import ValidationError


# class Customer(models.Model):
#     username = models.CharField(max_length=50, null=False)
#     password = models.CharField(max_length=50, null=False)
#     email = models.EmailField(null=False)

# class CustomerProfile(models.Model):
#     customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=150, null=False)
#     last_name = models.CharField(max_length=200, null=False)
#     phone = models.CharField(max_length=11, null=True, blank=True)

# superuser admin
# username : admin
# email : admin@gmail.com
# password : %r88rqV2]tHc

# user
# username : suchaya
# email : suchaya@gmail.com
# password : 6wGU>-5c1<

class SignUpView(View):

    # [หน้าที่]
    # - GET  : แสดงฟอร์มสมัครสมาชิก
    # - POST : ตรวจฟอร์ม, สร้างผู้ใช้ใหม่, แจ้งข้อความ, redirect ไปหน้า login

    def get(self, request):
        return render(request, "authen/signup.html", {"sign_up_form": SignUpForm()})

    def post(self, request):
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            return redirect('login')  # กลับไปหน้า login หลังสมัครเสร็จ
        return render(request, "authen/signup.html", {"sign_up_form" : sign_up_form})


class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('appointment_create')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html", {"form": form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')