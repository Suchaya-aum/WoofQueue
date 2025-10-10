from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()
# get_user_model() คืนค่า “คลาส User ปัจจุบัน” ของโปรเจกต์

#UserCreationForm ฟอร์มสมัครสมาชิกมาตรฐานของ Django
# มี field username, password1, password2 และตรวจ “รหัสผ่านตรงกัน” ให้
# ตอน form.save() จะ hash password ให้อัตโนมัติ
class SignUpForm(UserCreationForm):

    # [หน้าที่]
    # - ฟอร์ม SignUp
    # - สืบทอดจาก UserCreationForm (ช่วยเช็ก password1/password2 ให้)
    # - เพิ่ม field email และบังคับไม่ให้ซ้ำ
    # - เช็คความปลอดภัยของ password
    
    email = forms.EmailField(required=True)
    widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border border-gray-300 p-2 focus:ring-2 focus:ring-blue-400 ',
            'placeholder': 'Enter your email'
        })

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-800',
                'placeholder': 'Enter username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full rounded-lg border-gray-300',
                'placeholder': 'Enter password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full rounded-lg border-gray-300',
                'placeholder': 'Confirm password'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been used.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if password.isdigit():
            raise ValidationError("Password cannot be only numbers.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("Passwords must match exactly.")
        return cleaned_data
