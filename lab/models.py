from django.db import models
from tinymce.models import HTMLField
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
    

class Test(models.Model):
    name = models.CharField(max_length=100)
    low_ref = models.CharField(max_length=30,  null=True, blank=True)
    high_ref = models.CharField(max_length=30,  null=True, blank=True)
    elabaorated_range = HTMLField(blank=True, null=True,)
    notes =  HTMLField(blank=True, null=True,)
    amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)

class Package(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    linked_test = models.ManyToManyField(Test)

    class Meta: 
        ordering = ['name']

    def __str__(self):
        return self.name