from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.db import models
from devices.models import Device

# class Customer(models.Model):
#     email           =   models.EmailField()
#     phone_number    =   PhoneNumberField()
#
#
#
#     def __str__(self):
#         return self.email


class Contact(models.Model):
    email = models.EmailField()
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.email

class Address(models.Model):
    device          = models.OneToOneField(Device,on_delete=models.CASCADE)
    address_line_1  = models.CharField(max_length=120,help_text="description of the address also")
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    postal_code     = models.CharField(max_length=120)
    city            = models.CharField(max_length=120)
    state           = models.CharField(max_length=120)



    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}".format(
            line1 = self.address_line_1,
            line2 = self.address_line_2 or "",
            city    = self.city,
            state   = self.state
        )

"link the contact details to device for now"