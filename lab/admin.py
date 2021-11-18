from django.contrib import admin
from django_admin_search.admin import AdvancedSearchAdmin
from .models import *
# Register your models here.
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path, include, re_path

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ImportExportActionModelAdmin

from .search_fields import *
from .resources import *
import json

class OrderInline( admin.StackedInline):
    
    raw_id_fields = ("referred_by", "consulted_by",)
    filter_horizontal = ('investigation_test',)
    model = Order
    extra = 0
    

    
    
class PatientAdmin(ImportExportActionModelAdmin, AdvancedSearchAdmin):
    resource_class = PatientResource
    list_display = [field.name for field in Patient._meta.fields ]
    list_display_links = ['first_name'] 
    search_form = PatientFormSearch
    inlines = (OrderInline,)
    readonly_fields = ["date",]
    date_hierarchy = 'date'
    ordering = ("-date",)
   
    # Inject chart data on page load in the ChangeList view
    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            Patient.objects.annotate(date_daily=TruncDay("date"))
            .values("date_daily")
            .annotate(y=Count("id"))
            .order_by("-date_daily")
        )

   
admin.site.register(Patient, PatientAdmin)


class DoctorAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Doctor._meta.fields ]
   list_display_links = ['first_name'] 
   search_form = DoctorFormSearch
   resource_class = DoctorResource
   
admin.site.register(Doctor, DoctorAdmin)

class TestResource(resources.ModelResource):
    class Meta:
        model = Test

class TestAdmin(ImportExportModelAdmin, AdvancedSearchAdmin):
   list_display = [field.name for field in Test._meta.fields ]
   list_display_links = ['name']
   search_form = TestFormSearch
   resource_class = TestResource
   
admin.site.register(Test, TestAdmin)



class PackageAdmin(AdvancedSearchAdmin):
   list_display = [field.name for field in Package._meta.fields ]
   filter_horizontal = ['linked_test']
   list_display_links = ['name']
   search_form = PackageFormSearch
   
   
   
admin.site.register(Package, PackageAdmin)


admin.site.site_header = 'Lab Management'
admin.site.site_title = 'Lab Management'
admin.site.index_title = 'Lab Management'


class ResultThroughInline(admin.TabularInline):
   
    model = ResultThrough
    extra = 0
    
class OrderAdmin(ImportExportMixin, AdvancedSearchAdmin):
    
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
   resource_class = OrderResource

   
   
   
admin.site.register(Order, OrderAdmin)



class ResultThroughAdmin(admin.ModelAdmin):
   list_display = [field.name for field in ResultThrough._meta.fields ]
   
   
   
   
admin.site.register(ResultThrough, ResultThroughAdmin)



class LabInformationAdmin(admin.ModelAdmin):
   list_display = [field.name for field in LabInformation._meta.fields ]
   list_display_links = ['name'] 
   
   
   
   
admin.site.register(LabInformation, LabInformationAdmin)











