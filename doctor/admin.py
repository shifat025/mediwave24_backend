from django.contrib import admin
from .models import Doctor,Specialization,Department,ProfessionalQualification,Experience,AvailableTime,Fee,NationID,ProfilePic
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Specialization)
admin.site.register(ProfessionalQualification)
admin.site.register(Department)
admin.site.register(Experience)
admin.site.register(AvailableTime)
admin.site.register(Fee)
admin.site.register(NationID)
admin.site.register(ProfilePic)
