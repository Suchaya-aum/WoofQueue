from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("appointment/create/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("service/", views.ServiceManagementView.as_view(), name="service"),
    path("service/create", views.ServiceCreateView.as_view(), name="service_create"),
    path("service/update/<int:pk>", views.ServiceUpdateView.as_view(), name="service_update"),
    path("invoice/", views.InvoiceView.as_view(), name="invoice"),


]