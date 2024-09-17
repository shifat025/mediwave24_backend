from .views import (
    DoctorRegistration,
    DoctorDetail,
    DoctorList,
    DoctorUpdate,
    ProfessionalQualificationView,
    ProfessionDetails,
    ProfessionalUpdate,
    ProfessionalDelete,
    Departmentview,
    DepartmentList,
    SpecializationView,
    ExperienceView,
    AvailabletimeView,
    FeeView,
    NationalIdView,
    ProfilePicView,
    ProfessionList

)
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('department',Departmentview)
router.register('specializaion' , SpecializationView)
router.register('experience', ExperienceView)
router.register('avaiable_time', AvailabletimeView)
router.register('fee',FeeView)
router.register('profile_pic', ProfilePicView)

urlpatterns = [
    path('',include(router.urls)),
    path('registration/', DoctorRegistration.as_view(), name="doctor_registration"),
    path('<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),
    path('list/', DoctorList.as_view(), name='doctor-list'),
    path('update/<int:pk>/', DoctorUpdate.as_view(), name='doctor-partial-update'),
    path('qualification/', ProfessionalQualificationView.as_view(), name='professinal_qualification'),
    path('qualification/<int:pk>/', ProfessionDetails.as_view(), name='professinal_details'),
    path('qualification/list/', ProfessionList.as_view(), name='professinal_list'),
    path('qualification/update/<int:pk>/', ProfessionalUpdate.as_view(), name='professional-qualification-update'),
    path('qualification/delete/<int:pk>/', ProfessionalDelete.as_view(), name='professional-qualification-delete'),
    path('department_list/', DepartmentList.as_view(),name='department_list'),
    path('national_id/', NationalIdView.as_view(), name='national_id')

]
