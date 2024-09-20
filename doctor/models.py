from django.db import models
from django.contrib.auth.models import User
# from patient.models import Patient
from autoslug import AutoSlugField

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    district = models.CharField(max_length=30)
    national_id_or_passport_number = models.IntegerField()
    doctor_registration_number = models.CharField(max_length=40)
    doctor_type = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.title}"
    
class ProfessionalQualification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=30)
    institue_name = models.CharField(max_length=50)
    institue_location = models.CharField(max_length=50)
    passing_year = models.DateField()
    duration = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

class Department(models.Model):
    doctor = models.ManyToManyField(Doctor)
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)  # AutoSlugField

    def __str__(self):
        return self.name

class Specialization(models.Model):   
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True )
    specializanation = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)
    certification_type = models.CharField(max_length=30, null = True)   # Traning cirtificat
    document = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True) #prove to uploading cirtificate

    def __str__(self):
        return self.name
       
    
class Experience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hosspital_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    employee_period_start = models.DateField()
    employee_period_end = models.DateField()

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"
    
class AvailableTime(models.Model):
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    day = models.CharField(max_length=50)
    time_start = models.TimeField()
    time_end = models.TimeField()
    def __str__(self):
        return f"{self.day}: {self.time_start} - {self.time_end}"


class Fee(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    regular_fee = models.CharField(max_length=30)
    folowup_fee = models.CharField(max_length=30,blank=True,null=True)
    discount_fee = models.CharField(max_length=30,blank=True,null=True)
    free = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    followup = models.BooleanField(default=False)
    consultation_duration = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

class NationalID(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

class ProfilePic(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

