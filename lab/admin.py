from django.contrib import admin
from django_admin_search.admin import AdvancedSearchAdmin
from .models import *
# Register your models here.

from .search_fields import *



class OrderInline(admin.TabularInline):
   
    raw_id_fields = ("referred_by", "consulted_by",)
    filter_horizontal = ('investigation_test',)
    model = Order
    extra = 1
    

    
    
class PatientAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Patient._meta.fields ]
   search_form = PatientFormSearch
   inlines = (OrderInline,)
   
   
admin.site.register(Patient, PatientAdmin)


class DoctorAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Doctor._meta.fields ] 
   search_form = DoctorFormSearch
   
   
admin.site.register(Doctor, DoctorAdmin)


class TestAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Test._meta.fields ]
   search_form = TestFormSearch
   
   
admin.site.register(Test, TestAdmin)



class PackageAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Package._meta.fields ]
   search_form = PackageFormSearch
   
   
   
admin.site.register(Package, PackageAdmin)


admin.site.site_header = 'Lab Management'
admin.site.site_title = 'Lab Management'
admin.site.index_title = 'Lab Management'


class OrderAdmin(AdvancedSearchAdmin):
   search_form = OrderFormSearch
   list_display = ['order_date', 'patient' ]

   
   
   
admin.site.register(Order, OrderAdmin)




