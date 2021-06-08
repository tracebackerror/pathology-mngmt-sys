from django.db import models

# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  null=True, blank=True)
    contact_no = models.CharField(max_length=10,  null=True, blank=True)
    email =  models.EmailField(max_length=70,blank=True, null=True,)
    prn = models.CharField(max_length=50,  null=True, blank=True)
    
    
    
class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  null=True, blank=True)
    contact_no = models.CharField(max_length=10,  null=True, blank=True)
    email =  models.EmailField(max_length=70,blank=True, null=True,)
    degree = models.CharField(max_length=10,  null=True, blank=True)
    
    cut = models.FloatField(default=0.0)
    