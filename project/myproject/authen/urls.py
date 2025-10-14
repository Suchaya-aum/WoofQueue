from django.urls import path

from .views import LoginView, LogoutView, SignUpView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authen/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authen/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authen/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authen/password_reset_complete.html"), name="password_reset_complete"),
]