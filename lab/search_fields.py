from .models import *
from django.forms import ModelForm, Form
from django.forms import DateField, CharField, ChoiceField, TextInput
from django.forms import *
from django.contrib.admin import widgets


class PatientFormSearch(Form):
    id = CharField(required=False)
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    contact_no = CharField(required=False)
    card_number = CharField(required=False)


class DoctorFormSearch(Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    contact_no = CharField(required=False)

    email = EmailField(required=False)
    degree = CharField(required=False)

    cut = FloatField(required=False)


class TestFormSearch(Form):
    id = CharField(required=False)
    name = CharField(required=False)
    low_ref = CharField(required=False)
    high_ref = CharField(required=False)

    amount = CharField(required=False)


class PackageFormSearch(Form):
    id = CharField(required=False)
    name = CharField(required=False)
    amount = DecimalField(required=False)


class OrderFormSearch(Form):
    id = CharField(required=False)
    order_date = DateTimeField(required=False, )
