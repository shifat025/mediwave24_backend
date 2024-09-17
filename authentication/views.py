from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .serializers import UserSerializer,Loginserializer
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
from doctor.models import Doctor



# Create your views here.

class UserRegistration(APIView):
    serializer_class = UserSerializer
    
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

class EmailVerification(View):
    def get(self,request,uid64,token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk = uid)    
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful. You can now log in.')
            return redirect('user_registration')
        else:
            messages.error(request, 'Email verification failed.')
        return HttpResponse('Email verification failed.')


class Loginview(APIView):
    def post(self,request):
        serializer = Loginserializer(data = self.request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticating the user with the provided credentials
            try:
                get_email = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': "Invalid Credentials"}, status=400)
            
            user = authenticate(username=get_email.username, password = password)
            if user:
                token, created = Token.objects.get_or_create(user = user)
                login(request, user)

                # Check if the user is a doctor
                if Doctor.objects.filter(user = user).exists():
                    role = 'doctor'
                elif user.is_staff:
                    role = 'manager'
                else:
                    role = 'user'
                return Response({'token': token.key, 'user_id': user.id, 'role' : role})
            else:
                return Response({'error': "Invalid Creadential"},status=400)            
        return Response(serializer.errors, status=400)
    
class UserUpdate(APIView):
    def patch(self,request,pk):
        try:
            user = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response({'error': "Invalid Credentials"}, status=400)
        
        # Update fields if provided
        if 'username' in request.data:
            user.username = request.data.get('username',user.username)
        if 'first_name' in request.data:
            user.first_name = request.data.get('first_name', user.first_name)
        if 'last_name' in request.data:
            user.last_name = request.data.get('last_name', user.last_name)
        if 'email' in request.data:
            new_email = request.data.get('email')
            # Check for email uniqueness
            if User.objects.filter(email=new_email).exclude(pk=pk).exists():
                return Response({'error': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email

        # Save updated user information
        user.save()

        user_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        return Response(user_data,status=status.HTTP_200_OK)
    
class ChangePassword(APIView):
    def post(self,request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if not old_password or not new_password or not confirm_new_password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password and save
        if new_password != confirm_new_password:
            return Response({'error': "Password doesn't matched"})
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

