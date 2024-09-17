from django.shortcuts import render
from .serializers import Paitentserializer
from .models import Patient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
# Create your views here.

class PatientView(APIView):
    serializers_class = Paitentserializer
    def post(self,request):
        serializer = self.serializers_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatientList(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = Paitentserializer

    def get_queryset(self):
        # Return only the patients created by the user
        return Patient.objects.filter(user = self.request.user)
        
class UpdatePatient(APIView):
    def putch(self,request,pk):
        try:
            patient = Patient.objects.get(pk = pk)
        except Patient.DoesNotExist:
            return Response({'error': "Invalid Patient"}, status=400)
        
        if 'image' in request.data:
            patient.image = request.data.get('image', patient.image)
        if 'name' in request.data:
            patient.name = request.data.get('name',patient.name)
        if 'gender' in request.data:
            patient.gender = request.data.get('gender',patient.gender)
        if 'date_of_birth' in request.data:
            patient.date_of_birth = request.data.get('date_of_birth',patient.date_of_birth)
        if 'relation' in request.data:
            patient.relation = request.data.get('relation',patient.relation)
        if 'hight' in request.data:
            patient.hight = request.data.get('hight',patient.hight)
        if 'weight' in request.data:
            patient.weight = request.data.get('weight',patient.weight)
        if 'bloodgroup' in request.data:
            patient.bloodgroup = request.data.get('bloodgroup',patient.bloodgroup)

        patient.save()
        
        patient_data = {
            'image': patient.image,
            'name': patient.name,
            'gender': patient.gender,
            'date_of_birt': patient.date_of_birth,
            'relation': patient.relation,
            'hight': patient.hight,
            'weight': patient.weight,
            'bloodgroup': patient.bloodgroup
        }
        return Response(patient_data,status=status.HTTP_200_OK)
    

