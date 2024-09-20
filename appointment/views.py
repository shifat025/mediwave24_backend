from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
from patient.models import Patient

class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            # Get the Patient instance related to the currently authenticated User
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = request.user.doctor # Assuming the user is authenticated and has a related Doctor object
        appointments = Appointment.objects.filter(docter=doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    

class UpdateAppoinment(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id, docter=request.user.doctor)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        appointment.appointment_status = request.data.get('appointment_status', appointment.appointment_status)
        appointment.save()
        return Response({'message': 'Appointment status updated'})


