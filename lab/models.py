from django.db import models
from tinymce.models import HTMLField
# Create your models here.
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from .choice_option import *
from django.db.models import Count, Sum



class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  null=True, blank=True)
    contact_no = models.CharField(max_length=10,  null=True, blank=True)
    email =  models.EmailField(max_length=70,blank=True, null=True,)
    age = models.CharField(max_length=50,  null=True, blank=True)
    gender =   models.CharField(
        choices = GenderChoice.choices, 
        default= GenderChoice.MALE,
         max_length=100,)
    
    
    
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
    
    def __str__(self):
        return f"{self.name} - {self.amount}"
            

class Package(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    linked_test = models.ManyToManyField(Test)

    class Meta: 
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.amount}"
        

        
class Order(models.Model):

    order_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    referred_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name="referred_by")
    consulted_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name="consulted_by")
    sample_collected_at = models.CharField(
        choices=SampleCollectionType.choices,
        default=SampleCollectionType.LAB,
        max_length=100,
    )
    sample_collection_datetime = models.DateTimeField(default=datetime.now, blank=True, null=True)
    
    investigation_test = models.ManyToManyField(Test, null=True, blank=True)
    investigation_package = models.ManyToManyField(Package, null=True, blank=True)
    
    investigation_amount =  models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    visiting_charge =  models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    other_charge =  models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    discount_amount =  models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    
    final_amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    advance_received =  models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    balance_amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    
    
    payment_type =  models.CharField(
        choices=PaymentType.choices,
        default=PaymentType.CASH,
        max_length=100,
    )
    payment_notes =  models.TextField()
    
    
    
    
    