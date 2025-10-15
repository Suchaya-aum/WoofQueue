from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path("appointment/create/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("appointment/create/new_customer", views.NewCustomerView.as_view(), name="create_new_customer"),
    path("service/", views.ServiceManagementView.as_view(), name="service"),
    path("service/create", views.ServiceCreateView.as_view(), name="service_create"),
    path("service/update/<int:pk>", views.ServiceUpdateView.as_view(), name="service_update"),
    path("invoice/", views.InvoiceView.as_view(), name="invoice"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("appointment/create_booking/", views.BookingCreateView.as_view(), name="booking_request"),
    path("pet/create/", PetCreateView.as_view(), name="create_pet"),
    path("appointment/<int:pk>/edit/", AppointmentUpdateView.as_view(), name="appointment_update"),
    path("appointment/<int:pk>/booking_update/", BookingUpdateView.as_view(), name="booking_update"),
    path("appointment/<int:pk>/delete/", AppointmentDeleteView.as_view(), name="appointment_delete"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path('manage/customers/', ManageCustomerView.as_view(), name='manage_customer'),
    path('customer/edit/', CustomerProfileUpdateView.as_view(), name='customer_profile_edit'),
    path('pet/<int:pk>/edit/', PetUpdateView.as_view(), name='pet_edit'),
    path("customers/", ManageCustomerView.as_view(), name="manage_customer"),
    path("customer/<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer_update"),
    path("customer/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer_delete"),
    path("pet/<int:pk>/edit-admin/", PetUpdateAdminView.as_view(), name="pet_update_admin"),
]