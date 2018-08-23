from .models import Address,Contact
from django.forms import forms,ModelForm


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'postal_code', 'city','state']


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['phone_number', 'email']
