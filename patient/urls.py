from django.urls import path
from .views import PatientList,PatientView,UpdatePatient

urlpatterns = [
    path('', PatientView.as_view(), name='patients'),
    path('list/', PatientList.as_view(), name='patient_list'),
    path('update/<int:pk>', UpdatePatient.as_view(), name='patient_update'),
]