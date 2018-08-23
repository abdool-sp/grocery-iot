from django.contrib import admin

# Register your models here.
from .models import Address,Contact

admin.site.register(Contact)
admin.site.register(Address)