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


class ResultThroughInline(admin.TabularInline):
   
    model = ResultThrough
    extra = 0
    
class OrderAdmin(AdvancedSearchAdmin):
    
   def formfield_for_manytomany(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # TODO(dmu) MEDIUM: Remove `auto_created = True` after these issues are fixed:
        #                   https://code.djangoproject.com/ticket/12203 and
        #                   https://github.com/django/django/pull/10829

        # We trick Django here to avoid `./manage.py makemigrations` produce unneeded migrations
        ResultThrough._meta.auto_created = True  
        return super().formfield_for_manytomany(*args, **kwargs)

   search_form = OrderFormSearch
   list_display = ['order_date', 'patient' ]
   filter_horizontal = ('investigation_test', 'investigation_package')
   inlines = (ResultThroughInline,)
   date_hierarchy = 'order_date'

   
   
   
admin.site.register(Order, OrderAdmin)



class ResultThroughAdmin(admin.ModelAdmin):
   list_display = [field.name for field in ResultThrough._meta.fields ]
   
   
   
   
admin.site.register(ResultThrough, ResultThroughAdmin)



class LabInformationAdmin(admin.ModelAdmin):
   list_display = [field.name for field in LabInformation._meta.fields ]
   
   
   
   
admin.site.register(LabInformation, LabInformationAdmin)





