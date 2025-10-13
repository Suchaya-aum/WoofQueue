from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path("appointment/create/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("service/", views.ServiceManagementView.as_view(), name="service"),
    path("service/create", views.ServiceCreateView.as_view(), name="service_create"),
    path("service/update/<int:pk>", views.ServiceUpdateView.as_view(), name="service_update"),
    path("invoice/", views.InvoiceView.as_view(), name="invoice"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("appointment/create_booking/", views.BookingCreateView.as_view(), name="booking_request"),
    path("pet/create/", PetCreateView.as_view(), name="create_pet"),
    path("appointments/<int:pk>/edit/", AppointmentUpdateView.as_view(), name="appointment_update"),
    path("appointments/<int:pk>/delete/", AppointmentDeleteView.as_view(), name="appointment_delete"),
]