from lab.utils import convert_html_to_pdf, get_report_context
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, CreateView
from django.contrib.auth.views import LoginView
from .models import ResultThrough, Order
from .forms import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import decimal


class UserLogin(LoginView):
    template_name = 'lab/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        print(self.template_name)
        if request.user.is_authenticated:
            return redirect("lab:dashboard")
        return super().get(request, *args, **kwargs)

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("lab:login")


class Report(LoginRequiredMixin, TemplateView):
    template_name = "lab/report.html"
    extra_context = {}
    login_url = reverse_lazy('lab:login')

    def get(self, request, *args, **kwargs):
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None
        order_id = request.GET.get("order_id", None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
            else:
                messages.error(request, "Invalid Order ID, kindly check once")
        return super().get(request, *args, **kwargs)


class Invoice(LoginRequiredMixin, TemplateView):
    template_name = "lab/invoice.html"
    extra_context = {}
    login_url = reverse_lazy('lab:login')

    def get(self, request, *args, **kwargs):
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None
        order_id = request.GET.get("order_id", None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                order_obj.save()
                order_obj = Order.objects.get(id=order_id)
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
            else:
                messages.error(request, "Invalid Order ID, kindly check once")
        return super().get(request, *args, **kwargs)


class EReport(LoginRequiredMixin, TemplateView):
    template_name = "lab/e_report.html"
    extra_context = {}
    login_url = reverse_lazy('lab:login')

    def get(self, request, *args, **kwargs):
        if settings.ABS_URL is None:
            scheme = request.scheme
            host = request.get_host()
            settings.ABS_URL = f"{scheme}://{host}/"
        self.extra_context['order_obj'] = None
        self.extra_context['lab_info'] = None

        order_id = request.GET.get("order_id", None)
        download = request.GET.get("download", None)
        send_mail = request.GET.get("send_mail", None)
        if order_id:
            order_obj = Order.objects.filter(id=order_id)
            if order_obj:
                order_obj = order_obj.first()
                report_context = get_report_context(order_obj)
                self.extra_context.update(report_context)
                pdf = convert_html_to_pdf(
                    self.template_name, self.extra_context)
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"e-Report - {order_obj.patient.first_name} {order_obj.patient.last_name}.pdf"
                if download == "true":
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                elif send_mail == "true":
                    subject = f"e-Report - {self.extra_context['lab_info'].name}"
                    body = """Dear, {0} {1}
Your report has been out, you can see it by opening the attached PDF.
                    """.format(order_obj.patient.first_name, order_obj.patient.last_name)
                    to = order_obj.patient.email
                    msg = EmailMultiAlternatives(subject, body, None, [to])
                    msg.attach(filename, pdf, "application/pdf")
                    msg.send()
                    success_msg = f"e-Report has been sent Successfully to {order_obj.patient.email}. If they don't receive an email, please make sure email is correct, and check spam folder"
                    messages.success(request, success_msg,
                                     extra_tags="success")
                    return redirect(reverse_lazy("lab:report")+"?order_id="+order_id)
                return response
            else:
                messages.error(request, "Invalid Order ID, kindly check once")
        return redirect("lab:report")


# Ajax Request
class UpdateReport(View):
    def post(self, request, *args, **kwargs):
        response = {"status": 403, "msg": "FORBIDDEN"}
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
        response = {"status": 405, "msg": "METHOD_NOT_ALLOWED"}
        return JsonResponse(response)

# Ajax Request


class UpdateInvoice(View):
    def post(self, request, *args, **kwargs):
        response = {"status": 403, "msg": "FORBIDDEN"}
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
        response = {"status": 405, "msg": "METHOD_NOT_ALLOWED"}
        return JsonResponse(response)


class TakeOrder(LoginRequiredMixin, TemplateView):
    template_name = "lab/take_order.html"
    extra_context = {}
    login_url = reverse_lazy('lab:login')

    def get(self, request, *args, **kwargs):
        patient = request.GET.get("patient", "")
        if patient:
            patient_instance = Patient.objects.get(id=int(patient))
            pform = PatientForm(instance=patient_instance)
        else:
            pform = PatientForm()
        oform = OrderForm()
        self.extra_context["pform"] = pform
        self.extra_context["oform"] = oform
        self.extra_context["patient"] = patient
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        patient = request.POST.get("patient", "")
        if patient:
            patient_obj = Patient.objects.get(id=int(patient))
            pform = PatientForm(request.POST, instance=patient_obj)
        else:
            pform = PatientForm(request.POST)

        oform = OrderForm(request.POST)
        if oform.is_valid() and pform.is_valid():
            patient_obj = pform.save()
            order_obj = oform.save(commit=False)
            order_obj.patient = patient_obj
            order_obj.save()
            oform.save_m2m()
            return redirect(f"{reverse_lazy('lab:invoice')}?order_id={order_obj.id}")
        else:
            self.extra_context["pform"] = pform
            self.extra_context["oform"] = oform
            return super().get(request, *args, **kwargs)


class UpdateOrder(LoginRequiredMixin, TemplateView):
    template_name = "lab/update_order.html"
    extra_context = {}
    login_url = reverse_lazy('lab:login')
    success_url = reverse_lazy("lab:manage_order")
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs[self.pk_url_kwarg]
        order_obj = Order.objects.get(id=pk)
        pform = PatientForm(instance=order_obj.patient)
        oform = OrderForm(instance=order_obj)
        self.extra_context["pform"] = pform
        self.extra_context["oform"] = oform
        self.extra_context["order_obj"] = order_obj
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs[self.pk_url_kwarg]
        order_obj = Order.objects.get(id=pk)
        pform = PatientForm(request.POST, instance=order_obj.patient)
        oform = OrderForm(request.POST, instance=order_obj)
        if pform.is_valid() and oform.is_valid():
            pform.save()
            oform.save()
            order_obj.save()
            return redirect(self.success_url)
        else:
            self.extra_context["pform"] = pform
            self.extra_context["oform"] = oform
            self.extra_context["order_obj"] = order_obj
        return render(request, self.template_name, context=self.extra_context)


class ManageOrder(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('lab:login')
    template_name = "lab/manage_order.html"
    extra_context = {}
    model = Order
    ordering = "-order_date"
    context_object_name = "order_list"
