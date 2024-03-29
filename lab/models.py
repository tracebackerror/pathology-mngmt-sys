from django.db import models
from tinymce.models import HTMLField
# Create your models here.
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from .choice_option import *
from django.db.models import Count, Sum
from filer.fields.image import FilerImageField
from jsignature.fields import JSignatureField
from mptt.models import MPTTModel, TreeForeignKey


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  null=True, blank=True)
    contact_no = models.CharField(max_length=10,  null=True, blank=True)
    email =  models.EmailField(max_length=70,blank=True, null=True,)
    age = models.CharField(max_length=50,  null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=20,  null=True, blank=True)
    city = models.CharField(max_length=20,  null=True, blank=True)
    pincode = models.CharField(max_length=8,  null=True, blank=True)

    gender =   models.CharField(
        choices = GenderChoice.choices, 
        default= GenderChoice.MALE,
         max_length=100,)

    alternate_contact_person = models.CharField(max_length=20, null=True, blank=True)
    number_of_family = models.CharField(max_length=4,  null=True, blank=True)
    name_of_family_member = models.TextField(null=True, blank=True)
    registered_by = models.CharField(max_length=20, null=True, blank=True)
    referred_by = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    signature = JSignatureField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} - {self.contact_no}"
    
    
class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,  null=True, blank=True)
    contact_no = models.CharField(max_length=10,  null=True, blank=True)
    email =  models.EmailField(max_length=70,blank=True, null=True,)
    degree = models.CharField(max_length=10,  null=True, blank=True)
    
    cut = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.id} - {self.first_name} - {self.contact_no}"
    

class Test(MPTTModel):
    name = models.CharField(max_length=100)
    low_ref = models.CharField(max_length=30,  null=True, blank=True)
    high_ref = models.CharField(max_length=30,  null=True, blank=True)
    units = models.CharField(max_length=30,  null=True, blank=True)
    elabaorated_range = models.TextField(blank=True, null=True)
    notes =  models.TextField(blank=True, null=True)
    amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.name} - {self.amount}"

    class MPTTMeta:
        order_insertion_by = ['name']


class Package(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField( default=0.0, max_digits=10, decimal_places=2)
    linked_test = models.ManyToManyField(Test)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    
    investigation_test = models.ManyToManyField(Test, null=True, blank=True, through='ResultThrough')
    investigation_package = models.ManyToManyField(Package, null=True, blank=True, )
    
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
    payment_notes =  models.TextField(null=True, blank=True,)
    
    
    def __str__(self):
        return f"{self.id}"
    
    
class ResultThrough(models.Model):
    report_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    #order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    #results =  models.JSONField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=False)
    Test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=False, null=False)
    results =  models.CharField(max_length=200, default="NA")
    
    class Meta:
        # TODO(dmu) MEDIUM: Remove `auto_created = True` after these issues are fixed:
        #                   https://code.djangoproject.com/ticket/12203 and
        #                   https://github.com/django/django/pull/10829
        # Comment While Doing Make Migrations
        auto_created = True
        # Uncomment While Doing Make Migrations
        # spass





class LabInformation(models.Model):
    name = models.CharField(max_length=200, default="LAB")
    address = models.TextField(blank=True, null=True)
    checked = models.CharField(max_length=200, default="Checked By")
    doctor_name = models.CharField(max_length=200, blank=True, null=True)
    doctor_qualification = models.CharField(max_length=200, blank=True, null=True)
    doctor_post = models.CharField(max_length=200, blank=True, null=True)
    doctor_sign = FilerImageField(null=True, blank=True, on_delete=models.CASCADE,)
    
    header = models.TextField(blank=True, null=True)
    footer = models.TextField(blank=True, null=True)
    
    
    
    