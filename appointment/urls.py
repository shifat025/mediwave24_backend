from django.urls import path
from .views import CreateAppointmentView, DoctorAppointmentView,UpdateAppoinment

urlpatterns = [
    path('create/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('doctor/', DoctorAppointmentView.as_view(), name='doctor_appointments'),
    path('doctor/<int:appointment_id>/', UpdateAppoinment.as_view(), name='update_appointment_status'),
]
