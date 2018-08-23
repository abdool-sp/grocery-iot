from django.contrib import admin

# Register your models here.
from .models import Device,Slot

admin.site.register(Device)
admin.site.register(Slot)

