from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

#This class will also contain the list of names of the doctors who work for the hospital
class MusicAdmin(models.Model):
	first_name = models.CharField(max_length=256, default="")
	last_name = models.CharField(max_length=256, default="")
	user = models.OneToOneField(User, unique=True, blank=False, default="", null=False)

	def __unicode__(self):
		return str(self.first_name.title() + ' ' + str(self.last_name.title()))

class PermissionsRole(models.Model):
	role = models.CharField(max_length=256, choices=[('admin', 'admin'), ('patient', 'patient')])
	user = models.OneToOneField(User, unique=True,  blank=True, default="")

	def __unicode__(self):
		return str(self.role)

#This is the mediator for the data that is submitted by the user to the HSP staff
#The data is stored and if admin approves user, then the data will be stored into a patient class
class TempPatientData(models.Model):

	user = models.OneToOneField(User,unique=True,null=True,default="")
	email_address = models.CharField(max_length=256, blank=False)
	first_name = models.CharField(max_length=256, default="")
	last_name = models.CharField(max_length=256, default="")
	age = models.IntegerField(default = 18, blank=False)
	gender = models.CharField(max_length=256, choices=[('male','Male'), ('female', 'Female'), ('other', 'Other'), ('prefer not to say', 'Prefer Not To Say')], default='Select a gender', blank = False)
	data_sent = models.IntegerField(default=0)


	def __unicode__(self):
		return (str(self.first_name) + " " + str(self.last_name) + " " + str(self.email_address))

#This patient model will extend the user class so we can add the associated medical data for the user
class Patient(models.Model):

	fill_from_application = models.OneToOneField(TempPatientData,unique=True,null=True,default="")
	user = models.OneToOneField(User, unique=True,  blank=True, default="", null=True)
	approved = models.IntegerField(default=0, null=False)
	alertSent = models.IntegerField(default=0, null=False)
	date_created = models.CharField(default="9-20-1995", null=True, max_length=20)


	def __unicode__(self):
		return 'Email: ' + str(self.user) + ' First Name: ' + str(self.fill_from_application.first_name) + ' Last Name: ' + str(self.fill_from_application.last_name)

class PatientHealthConditions(models.Model):

	user = models.OneToOneField(Patient, unique=False, blank=True, default="")

	#nausea_level = models.IntegerField(validators=[MinValueValidator(0),
    #                                  MaxValueValidator(10)], default=0)
	def __unicode__(self):
		return str(self.user.user.username)

#Class for the user to schedule appointments for their associated doctor
class PatientAppt(models.Model):
	date = models.CharField(max_length=1000, unique=True)
	doctor = models.ForeignKey(MusicAdmin, unique=False, default=-1)
	pain_level = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(10)], blank=False)
	medical_conditions = models.CharField(max_length=1000, default="None")
	allergies = models.CharField(max_length=1000, default="None")
	user = models.ForeignKey(Patient, unique=False, blank=True, default="")
	current_health_conditions = models.ForeignKey(PatientHealthConditions, unique=False, blank=True, default="", null=True)
	resolved = models.IntegerField(default=0, blank=True)

	def __unicode__(self):
		return str(self.doctor)

#Class that is responsible for housing all of the alerts that are submitted by the user
class Alert(models.Model):
	alert_level = models.IntegerField(default=0, null=False)
	alert_patient = models.OneToOneField(Patient, unique = True, null = True)
	alert_description = models.CharField(max_length=255, default="", null = True, unique=False)

class EMedication(models.Model):
	patient = models.ForeignKey(Patient, null=False, default='', blank=False)
	medication_name = models.CharField(max_length=255, default = '', blank=False, null=False)
	medication_quantity = models.IntegerField(default=0, blank=True, null=True)
	reminder = models.IntegerField(default=0)
	prescribed_by_doctor = models.ForeignKey(MusicAdmin, default="0")

class LabReport(models.Model):
	lab_patient = models.ForeignKey(Patient, default = "0")
	lab_results = models.CharField(max_length=255, choices=[('positive', 'Positive'), ('negative', 'Negative')])
	lab_test = models.CharField(max_length=255, choices=[('Blood pressure screening', 'Blood pressure screening'), ('C-reactive protein test', 'C-reactive protein test'), ('Colonoscopy', 'Colonoscopy'), ('Diabetes risk tests', 'Diabetes risk tests'), ('Pap smear', 'Pap smear'), ('Skin cancer exam', 'Skin cancer exam'), ('Blood Tests', 'Blood Tests')])
	lab_notes = models.TextField(default="Insert Notes For Lab Test")
	

class AddMedicalHistory(models.Model):
	allergies = models.CharField(max_length=255, default="")
	medical_conditions = models.CharField(max_length=255, default="")
	patient = models.ForeignKey(Patient, default="")

