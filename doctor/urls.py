from .views import DoctorRegistration,DoctorDetail,DoctorList,DoctorUpdate
from django.urls import path

urlpatterns = [
    path('registration/', DoctorRegistration.as_view(), name="doctor_registration"),
    path('<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),
    path('list/', DoctorList.as_view(), name='doctor-list'),
    path('update/<int:pk>/', DoctorUpdate.as_view(), name='doctor-partial-update'),
]
