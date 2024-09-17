from django.db import models
from django.contrib.auth.models import User
from doctor.models import Doctor
# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient/media/uploads', blank = True, null = True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    relation = models.CharField(max_length=10)
    hight = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    bloodgroup = models.CharField(max_length=10)

star_choice = [
    ('⭐','1'),
    ('⭐⭐','2'),
    ('⭐⭐⭐','3'),
    ('⭐⭐⭐⭐','4'),
    ('⭐⭐⭐⭐⭐','5'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    docter = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    ratting = models.CharField(choices=star_choice,max_length=10)

    def __str__(self):
        return f"Patient: {self.reviewer.user.first_name}; Doctor: {self.docter.user.first_name}"