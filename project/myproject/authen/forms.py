# forms.py
from django import forms
from django.core.exceptions import ValidationError

# ของ Django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

# CustomerProfile
from app.models import CustomerProfile


# Sign Up 
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border border-gray-300 p-2',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        # UserCreationForm มี password1/password2 
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Enter email'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Enter password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Confirm password'
            }),
        }


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email has already been used.")
        return email

    def save(self, commit=True):
        # UserCreationForm จะ hash password ให้อัตโนมัติแล้ว
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# Login 
# ใช้ AuthenticationForm จะจัดการตรวจ hash + authenticate ให้ครบ
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full border-gray-300 rounded-lg',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border-gray-300 rounded-lg',
            'placeholder': 'Password'
        })
    )

# Profile 
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["first_name", "last_name", "phone"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Enter first name'}),
            'last_name':  forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2',
                'placeholder': 'Enter last name'}),
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")
            if len(phone) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean(self):
        cleaned = super().clean()
        first = cleaned.get("first_name")
        last = cleaned.get("last_name")
        if not first or not last:
            raise ValidationError("Please fill both first name and last name.")
        return cleaned
