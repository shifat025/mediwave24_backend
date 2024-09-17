from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Doctor

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    # User-related fields
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # Doctor-specific fields
    title = serializers.CharField(max_length=30)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=20)
    district = serializers.CharField(max_length=30)
    national_id_or_passport_number = serializers.CharField(max_length=40)
    doctor_registration_number = serializers.CharField(max_length=40)
    doctor_type = serializers.CharField(max_length=30)
    mobile_number = serializers.CharField(max_length=11)
    available_time = serializers.CharField(max_length=100)

    class Meta:
        model = Doctor
        fields = [
            'username','first_name','last_name','email','password','confirm_password', 'title', 'date_of_birth', 'gender', 'district', 
            'national_id_or_passport_number', 'doctor_registration_number', 
            'doctor_type', 'mobile_number', 'available_time'
        ]

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': "Passwords do not match"})
        
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': "Email already exists"})

        return data
    
    def create(self, validated_data):
        # Extract user-related data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')


        # Create user
        account = User.objects.create(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            email=email
        )
        account.set_password(password)
        account.is_active = False
        account.save()

        # Create doctor profile linked to the user
        doctor = Doctor.objects.create(user=account, **validated_data)
        return account
    
class DoctorUpdataSerializer(serializers.ModelSerializer):
    # Fields related to the User model
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField(required=False)
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'title', 'gender', 'district', 'doctor_type', 'mobile_number', 'available_time']

    def update(self, instance, validated_data):
        # Update the User model fields if provided
        user_data = {
            'first_name': validated_data.get('first_name', None),
            'last_name': validated_data.get('last_name', None),
            'email': validated_data.get('email', None),
        }
        for attr, value in user_data.items():
            if value is not None:
                setattr(instance.user, attr, value)
        instance.user.save()

        # Update the Doctor model fields if provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

       
