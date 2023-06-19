from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class' :'form-control',
        'placeholder': 'Username'
        }
    ),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' :'form-control',
        'placeholder': 'Password'
        }
    ),required=True)


class PatientForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}), required=True)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}), required=True)

    contact_no = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control", "min": "1111111111", "max": "9999999999"}), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control"}), required=False)

    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control"}), required=True)

    gender = forms.ChoiceField(widget=forms.Select(
        attrs={"class": "form-control"}), choices=GenderChoice.choices, required=True)

    class Meta:
        model = Patient
        exclude = ['date']


class OrderForm(forms.ModelForm):
    patient = forms.ModelChoiceField(widget=forms.Select(attrs={
        "class": "form-control"}), queryset=Patient.objects.all(), required=False)

    referred_by = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}), required=True, initial="Dr. ")

    consulted_by = forms.ModelChoiceField(widget=forms.Select(attrs={
        "class": "form-control"}), queryset=Doctor.objects.all(), required=True)

    sample_collected_at = forms.ChoiceField(widget=forms.Select(
        attrs={"class": "form-control"}), choices=SampleCollectionType.choices, required=True)

    sample_collection_datetime = forms.CharField(widget=forms.DateTimeInput(
        attrs={"class": "form-control"}), required=True)

    investigation_test = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"class": "form-control","style":"height:200px"}), queryset=Test.objects.all(), required=False)

    investigation_package = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"class": "form-control","style":"height:200px"}), queryset=Package.objects.all(), required=False)

    payment_type = forms.ChoiceField(widget=forms.Select(
        attrs={"class": "form-control"}), choices=PaymentType.choices, required=True)

    payment_notes = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control","rows":"2"}), required=False)

    class Meta:
        model = Order
        exclude = ['order_date', 'visiting_charge', 'investigation_amount', 'other_charge',
                   'discount_amount', 'final_amount', 'advance_received', 'balance_amount']
