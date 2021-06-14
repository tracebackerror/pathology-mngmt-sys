""" IMPORT EXPORT
"""
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *



class OrderResource(resources.ModelResource):

    class Meta:
        model = Order
        
class PatientResource(resources.ModelResource):

    class Meta:
        model = Patient
        
        
class DoctorResource(resources.ModelResource):

    class Meta:
        model = Doctor
        
        
class TestResource(resources.ModelResource):

    class Meta:
        model = Test