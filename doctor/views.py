from django.shortcuts import render,redirect
from rest_framework.views import APIView
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
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    DoctorRegistrationSerializer,
    DoctorUpdataSerializer,
    ProfessionalQualificationSerializer,
    ProfessionQualificationUpdateSerializer,
    DepartmentSerializer,
    SpecializationSerializer,
    ExperienceSerializer,
    AvailabletimeSerializer,
    FeeSerializer,
    NationalIdSerializer,
    ProfilePicSerializer

)
from .models import (
    Doctor,
    ProfessionalQualification,
    Department,
    Specialization,
    Experience,
    AvailableTime,
    Fee,
    NationalID,
    ProfilePic
)
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
            "mobile_number": doctor.mobile_number
            
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
            # "user_id": user.id,      # User's ID
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
            "mobile_number": doctor.mobile_number
           
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
    
class ProfessionalQualificationView(APIView):
    serializer_class = ProfessionalQualificationSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def post(self,request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                doctor = Doctor.objects.get(user = self.request.user)
            except Doctor.DoesNotExist:
                return Response({"error": "Doctor not found for this user.Try again"}, status=status.HTTP_404_NOT_FOUND)
            
            # Save the ProfessionalQualification with the doctor instance
            serializer.save(doctor = doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class ProfessionDetails(APIView):
    serializer_class = ProfessionalQualificationSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def get(self,request,pk):    
        try:
            professional_qualification = ProfessionalQualification.objects.get(pk = pk)
        except ProfessionalQualification.DoesNotExist:
            return Response({"error": "Doctor not found for this user.Try again"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data and return it in the response
        serializer = self.serializer_class(professional_qualification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ProfessionList(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the logged-in user
        
        try:
            doctor = Doctor.objects.get(user=user)  # Get the Doctor object associated with the user
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        qualifications = ProfessionalQualification.objects.filter(doctor=doctor)  # Filter by logged-in doctor

        if not qualifications.exists():
            return Response({"message": "No qualifications found"}, status=status.HTTP_204_NO_CONTENT)
        
        qualification_list = []

        for qualification in qualifications:
            qualification_data = {
                'id': qualification.id,
                'degree_name': qualification.degree_name,
                'institute_name': qualification.institue_name,
                'institue_location': qualification.institue_location,
                'passing_year': qualification.passing_year,  # Format the passing year
                'duration': qualification.duration
            }
            qualification_list.append(qualification_data)
        
        return Response(qualification_list, status=status.HTTP_200_OK)

class ProfessionalUpdate(APIView):
    serializer_class = ProfessionQualificationUpdateSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def patch(self,request,pk):
        try:
            # Retrieve the ProfessionalQualification instance
            professional_qualification = ProfessionalQualification.objects.get(pk=pk)
        except ProfessionalQualification.DoesNotExist:
            return Response({"error": "Professional Qualification not found.Try Again"}, status=status.HTTP_404_NOT_FOUND)

        # Partially update the instance with the request data
        serializer = self.serializer_class(professional_qualification, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfessionalDelete(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def delete(self, request, pk):
        try:
            # Retrieve the ProfessionalQualification instance
            professional_qualification = ProfessionalQualification.objects.get(pk=pk)
        except ProfessionalQualification.DoesNotExist:
            return Response({"error": "Professional Qualification not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the instance
        professional_qualification.delete()
        return Response({"message": "Professional Qualification deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class Departmentview(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def perform_create(self, serializer):
        user = self.request.user

        try:
            doctor = Doctor.objects.get(user=user)  # Get the Doctor object for the logged-in user
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(doctor=[doctor])  # Automatically assign the logged-in doctor


class DepartmentList(APIView):
    def get(self,request):
        departments = Department.objects.all()
        
        # Prepare the list to hold department data
        department_list = []

        # Iterate over each department instance and construct the data dictionary
        for department in departments:
            department_data = {
            'name' : department.name,
            'slug' : department.slug
        }
            department_data.append(department_data)

        # Return the list as a JSON response
        return Response(department_list, status=status.HTTP_200_OK)
    
class SpecializationView(ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def perform_create(self, serializer):
        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor)    
    

class ExperienceView(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def perform_create(self, serializer):
        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor) 

class AvailabletimeView(ModelViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailabletimeSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def perform_create(self, serializer):
        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor) 

class FeeView(ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def perform_create(self, serializer):
        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor) 

class NationalIdView(APIView):
    serializer_class = NationalIdSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_create(self, serializer):
        # When saving a new specialization, link it to the current doctor
        doctor = self.request.user.doctor  # Get the doctor linked to the logged-in user
        serializer.save(doctor=doctor)


class ProfilePicView(ModelViewSet):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
        
    def perform_create(self, serializer):
        user = self.request.user
        doctor = Doctor.objects.get(user=user)
        serializer.save(doctor=doctor) 











    