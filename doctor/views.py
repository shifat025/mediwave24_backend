from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .serializers import DoctorRegistrationSerializer,DoctorUpdataSerializer
from .models import Doctor
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
# Create your views here.

class DoctorRegistration(APIView):
    serializer_class = DoctorRegistrationSerializer
    
    def post(self,request):
        user_serializer = self.serializer_class(data = request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}/"
            email_subject = "Confirm your mail"
            email_body = render_to_string('confirm_email.html',{'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            messages.success(request, 'Registration successful. Check your mail for confirmation')
            # return redirect('login')
            return Response({"message": "Registration successful. Check your email for confirmation"}, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors)  
    
class DoctorDetail(APIView):
    # Retrieve the doctor's current information using GET request
    def get(self,request,pk):
        try:
            # Retrieve the doctor object using Doctor.objects.get()
            doctor = Doctor.objects.get(pk = pk)

        except Doctor.DoesNotExist:
            # Manually return a 404 response if doctor does not exist
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve the associated user details
        user = doctor.user

        # Create a manual response data dictionary
        doctor_data = {
            "doctor_id": doctor.id,  # Doctor's ID
            "user_id": user.id,      # User's ID
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "title": doctor.title,
            "date_of_birth": doctor.date_of_birth,
            "gender": doctor.gender,
            "district": doctor.district,
            "national_id_or_passport_number": doctor.national_id_or_passport_number,
            "doctor_registration_number": doctor.doctor_registration_number,
            "doctor_type": doctor.doctor_type,
            "mobile_number": doctor.mobile_number,
            "available_time": doctor.available_time
        }

        return Response(doctor_data, status=status.HTTP_200_OK)
    
class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()

        doctor_list = []

        for doctor in doctors:
            user = doctor.user

        doctor_data = {
            "doctor_id": doctor.id,  # Doctor's ID
            "user_id": user.id,      # User's ID
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "title": doctor.title,
            "date_of_birth": doctor.date_of_birth,
            "gender": doctor.gender,
            "district": doctor.district,
            "national_id_or_passport_number": doctor.national_id_or_passport_number,
            "doctor_registration_number": doctor.doctor_registration_number,
            "doctor_type": doctor.doctor_type,
            "mobile_number": doctor.mobile_number,
            "available_time": doctor.available_time
        }
        doctor_list.append(doctor_data)
        return Response(doctor_list, status=status.HTTP_200_OK)
    
class DoctorUpdate(APIView):
    def patch(self,request,pk):
        try:
            # Retrieve the doctor object using Doctor.objects.get()
            doctor = Doctor.objects.get(pk = pk)

        except Doctor.DoesNotExist:
            # Manually return a 404 response if doctor does not exist
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the related User object
        user = doctor.user

        serializer = DoctorUpdataSerializer(doctor,data = request.data)

        if serializer.is_valid():
            serializer.save()  # Save the updated fields
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)