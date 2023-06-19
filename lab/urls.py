from django.urls import path
from .views import *

app_name = "lab"

urlpatterns = [
    path("", TakeOrder.as_view(), name="dashboard"),
    path("login/", UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path("report/", Report.as_view(), name="report"),
    path("report/update/", UpdateReport.as_view(), name="update_report"),
    path("invoice/", Invoice.as_view(), name="invoice"),
    path("invoice/update/", UpdateInvoice.as_view(), name="update_invoice"),
    path("e-report", EReport.as_view(), name="e_report"),
    path("order/take/", TakeOrder.as_view(), name="take_order"),
    path("order/manage/", ManageOrder.as_view(), name="manage_order"),
    path("order/<int:pk>/update/", UpdateOrder.as_view(), name="update_order"),
]
