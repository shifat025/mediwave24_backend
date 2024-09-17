from .views import UserRegistration,EmailVerification,Loginview,UserUpdate
from django.urls import path

urlpatterns = [
    path("registration/", UserRegistration.as_view(), name="user_registration"),
    path('activate/<uid64>/<token>/', EmailVerification.as_view(), name='email-verification'),
    path('login/', Loginview.as_view(), name='Login'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user-update')
]
