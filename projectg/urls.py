"""projectg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from devices.views import deviceRegister,deviceView,slot_weight_endpoint,set_device_active_view,slot_fill_form
from addresses.views import regiteration_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', regiteration_view,name='registration'),
    path('register/slot/', slot_fill_form,name='slot-form'),
    path('slot/filling/', slot_weight_endpoint, name='slot-endpoint'),
    path('device/set_active/', set_device_active_view, name='active-endpoint'),
    path('home/', deviceView, name='home'),
    path('register/<device_id>/',deviceRegister,name='register'),
]
