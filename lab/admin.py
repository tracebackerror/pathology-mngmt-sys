from django.contrib import admin
from django_admin_search.admin import AdvancedSearchAdmin
from .models import *
# Register your models here.

from .search_fields import *



class PatientAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Patient._meta.fields ]
   search_form = PatientFormSearch
   
   
admin.site.register(Patient, PatientAdmin)


class DoctorAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Doctor._meta.fields ]
   search_form = DoctorFormSearch
   
   
admin.site.register(Doctor, DoctorAdmin)