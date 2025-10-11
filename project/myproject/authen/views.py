# superuser admin
# username : admin
# email : admin@gmail.com
# password : %r88rqV2]tHc

# user
# username : suchaya
# email : suchaya@gmail.com
# password : 6wGU>-5c1<

# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages

# ใช้ login/logout ของ Django จัดการ session ให้
from django.contrib.auth import login, logout

# SignUpForm: สืบทอดจาก UserCreationForm (hash password อัตโนมัติ)
# LoginForm: สืบทอดจาก AuthenticationForm (ตรวจ username/password + authenticate อัตโนมัติ)
from .forms import SignUpForm, CustomerProfileForm, LoginForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class SignUpView(View):
    def get(self, request):
        return render(request, 'authen/signup.html', {
            "c_form": SignUpForm(), # User (username/email/password1/password2)
            "p_form": CustomerProfileForm(), # Profile (first_name/last_name/phone)
        })

    @transaction.atomic  # transaction เดียว: พลาดตรงไหน rollback ทั้งหมด
    def post(self, request):
        c_form = SignUpForm(request.POST)
        p_form = CustomerProfileForm(request.POST)

        if c_form.is_valid() and p_form.is_valid():
            # 1 บันทึก User ก่อน (SignUpForm จัดการ hash ให้แล้ว)
            user = c_form.save()  # ถ้าใน SignUpForm.save() เราตั้ง commit=True ไว้ ก็จะ save จริงที่นี่

            # 2 เตรียมบันทึก profileโดยผูก FK -> User ที่เพิ่งสร้าง
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()

            # autologin หลังสมัครเสร็จ ให้แทนที่ 3 บรรทัดบนด้วย:
            login(request, user)
            return redirect('appointment')  # หรือหน้าไหนก็ได้

        # ถ้าไม่ผ่าน validation: ส่งกลับพร้อม error
        return render(request, 'authen/signup.html', {"c_form": c_form, "p_form": p_form})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'authen/login.html', {"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            # ถ้า valid: get_user() จะคืน User ที่ authenticate ผ่านแล้ว
            user = login_form.get_user()
            login(request, user)  # Django จะสร้าง session ให้เอง
            return redirect('appointment')
        else:
            # invalid  render หน้าเดิมพร้อม error
            return render(request, 'authen/login.html', {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
