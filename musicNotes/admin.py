from django.contrib import admin
from .forms import *
from .models import Patient, PatientAppt, PermissionsRole, MusicAdmin, TempPatientData

class PermissionsRoleAdmin(admin.ModelAdmin):
	list_display = ('user', 'role')

class TempPatientDataAdmin(admin.ModelAdmin):
	list_display=('first_name','last_name', 'gender')

class PatientAdmin(admin.ModelAdmin):
	list_display=('user', 'alertSent')
	# readonly_fields = ('created',)

admin.site.register(PermissionsRole, PermissionsRoleAdmin)
admin.site.register(TempPatientData,TempPatientDataAdmin)
admin.site.register(Patient, PatientAdmin)


