from django.urls import path
from .views import *

app_name="lab"

urlpatterns = [
    path("",Dashboard.as_view(),name="dashboard"),
    path("report/",Report.as_view(),name="report"),
    path("report/update/",UpdateReport.as_view(),name="update_report"),
    path("invoice/",Invoice.as_view(),name="invoice"),
    path("invoice/update/",UpdateInvoice.as_view(),name="update_invoice"),
    path("e-report",EReport.as_view(),name="e_report"),
]
