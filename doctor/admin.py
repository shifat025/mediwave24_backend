from django.contrib import admin
from .models import Doctor,Specialization,Department,ProfessionalQualification,Experience,AvailableTime,Fee,NationalID,ProfilePic
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Specialization)
admin.site.register(ProfessionalQualification)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Add slug to list display
    fields = ('name', 'slug')  # Show 'name' and 'slug' in the form
    readonly_fields = ('slug',)  # Mark 'slug' as read-only if it's auto-populated


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Experience)
admin.site.register(AvailableTime)
admin.site.register(Fee)
admin.site.register(NationalID)
admin.site.register(ProfilePic)
