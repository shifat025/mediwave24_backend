from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Dosen't Matched"})
        
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error': "Email Already exits"})
        
        account = User(username = username, first_name = first_name,last_name = last_name, email = email)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    
class Loginserializer(serializers.Serializer):
    email = serializers.CharField(max_length = 50)
    password = serializers.CharField(write_only=True)