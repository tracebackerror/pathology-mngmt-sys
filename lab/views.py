from lab.utils import convert_html_to_pdf, get_report_context
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from .models import ResultThrough, Order
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import decimal


class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = "lab/dashboard.html"
    extra_context = {}
    login_url = '/admin/login/'


class Report(LoginRequiredMixin,TemplateView):
    success_url = reverse_lazy("report")
    template_name = "lab/report.html"
    extra_context = {}
    login_url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None
        order_id = request.GET.get("order_id",None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
            else:
                messages.error(request,"Invalid Order ID, kindly check once")
        return super().get(request, *args, **kwargs)


class Invoice(LoginRequiredMixin,TemplateView):
    template_name = "lab/invoice.html"
    extra_context = {}
    login_url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None
        order_id = request.GET.get("order_id",None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                order_obj.save()
                order_obj = Order.objects.get(id=order_id)
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
            else:
                messages.error(request,"Invalid Order ID, kindly check once")
        return super().get(request, *args, **kwargs)


class EReport(LoginRequiredMixin,TemplateView):
    success_url = reverse_lazy("report")
    template_name = "lab/e_report.html"
    extra_context = {}
    login_url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        if settings.ABS_URL is None:
            scheme = request.scheme
            host = request.get_host()
            settings.ABS_URL = f"{scheme}://{host}/"
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None

        order_id = request.GET.get("order_id",None)
        download = request.GET.get("download",None)
        send_mail = request.GET.get("send_mail",None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
                pdf = convert_html_to_pdf(self.template_name, self.extra_context)
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"e-Report - {order_obj.patient.first_name} {order_obj.patient.last_name}.pdf"
                if download == "true":
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                elif send_mail == "true":
                    subject = f"e-Report - {self.extra_context['lab_info'].name}"
                    body = """Dear, {0} {1}
Your report has been out, you can see it by opening the attached PDF.
                    """.format(order_obj.patient.first_name,order_obj.patient.last_name)
                    to = order_obj.patient.email
                    msg = EmailMultiAlternatives(subject,body,None,[to])
                    msg.attach(filename, pdf, "application/pdf")
                    msg.send()
                    success_msg = f"e-Report has been sent Successfully to {order_obj.patient.email}. If they don't receive an email, please make sure email is correct, and check spam folder"
                    messages.success(request,success_msg,extra_tags="success")
                    return redirect(reverse_lazy("lab:report")+"?order_id="+order_id)
                return response
            else:
                messages.error(request,"Invalid Order ID, kindly check once")
        return redirect("lab:report")



### Ajax Request
class UpdateReport(View):
    def post(self, request, *args, **kwargs):
        response = {"status":403,"msg":"FORBIDDEN"}
        if request.is_ajax() and request.user.is_authenticated:
            result_id = int(request.POST['result_id'])
            result = request.POST['result']
            result_obj = ResultThrough.objects.get(id=result_id)
            result_obj.results = result
            result_obj.save()
            response["status"] = 200
            response["msg"] = "Result Updates Successfully"
        return JsonResponse(response)
    
    def get(self, request, *args, **kwargs):
        response = {"status":405,"msg":"METHOD_NOT_ALLOWED"}
        return JsonResponse(response)

### Ajax Request
class UpdateInvoice(View):
    def post(self, request, *args, **kwargs):
        response = {"status":403,"msg":"FORBIDDEN"}
        if request.is_ajax() and request.user.is_authenticated:
            order_id = int(request.POST['order_id'])
            field_id = int(request.POST['field_id'])
            value = decimal.Decimal(request.POST['value'])
            order_obj = Order.objects.get(id=order_id)
            if field_id == 1:
                order_obj.visiting_charge = value
            elif field_id == 2:
                order_obj.other_charge = value
            elif field_id == 3:
                order_obj.discount_amount = value
            elif field_id == 4:
                order_obj.advance_received = value
            order_obj.save()   
            order_obj = Order.objects.get(id=order_id)  
            response["final_amount"] = str(order_obj.final_amount)
            response["balance_amount"] = str(order_obj.balance_amount)
            response["status"] = 200
            response["msg"] = "Result Updates Successfully"
        return JsonResponse(response)
    
    def get(self, request, *args, **kwargs):
        response = {"status":405,"msg":"METHOD_NOT_ALLOWED"}
        return JsonResponse(response)