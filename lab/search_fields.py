from .models import *
from django.forms import ModelForm, Form
from django.forms import DateField, CharField, ChoiceField, TextInput
from django.forms import *

class PatientFormSearch(Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    contact_no = CharField(required=False)
    
    
class DoctorFormSearch(Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    contact_no = CharField(required=False)
    
    email =  EmailField(required=False)
    degree = CharField(required=False)
    
    cut = FloatField(required=False)
    
    
class TestFormSearch(Form):
    name = CharField(required=False)
    low_ref = CharField(required=False)
    high_ref = CharField(required=False)
    
    amount =  DecimalField(required=False)
    
    
class PackageFormSearch(Form):
    name = CharField(required=False)
    amount =  DecimalField(required=False)
    
    
class OrderFormSearch(Form):
    order_date = DateTimeField(required=False)
  