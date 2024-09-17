from rest_framework import serializers
from .models import Patient,Review

class Paitentserializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        field = '__all__'