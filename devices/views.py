from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from .models import Device

from addresses.models import Address,Contact
from addresses.forms import ContactForm,AddressForm

# Register a device


def deviceView(request):
    device_id = request.POST.get('device_id')   # device_id from form
    context = None
    if device_id is not None:
        device = Device.objects.filter(device_id=device_id).first()
        if not device.active:
            print("right here")
            url = "/register/" + str(device_id) + "/"
            print(url)
            return redirect("register",device_id=device_id)

        context = {'device': device }

    return render(request,template_name="device/detail_view.html", context=context)





def deviceRegister(request, device_id):
    dev = Device.objects.filter(device_id=device_id).first()

    dev_address,dev_contact = dev.has_related_object()
    addressForm = None
    contactForm = None

    if not dev_address:
        addressForm = AddressForm()

    if not dev_contact:
        contactForm = ContactForm()

    if dev_address or dev_contact:
        next_url = '/home/'
    else:
        next_url = request.build_absolute_uri


    context = {
        'dev': dev,
        'address_form': addressForm,
        'contact_form' : contactForm,
        'next_url' : next_url,
    }

    return render(request,template_name="device/register.html",context= context)



@csrf_exempt
def slot_weight_endpoint(request):
   if request.method == 'POST':
       print(json.dumps(request.POST))
       Id = request.POST.get("ID",None)
       try:
           device = Device.objects.get(device_id=Id)

           if not device.active:
               return HttpResponse("Device is not active",content_type="text/plain", status=200)
       except Device.DoesNotExist:
           return HttpResponse("Device is not found", content_type="text/plain",status=404)


       count = 1
       params = request.POST
       if params.get('action') == 'slot_filling':
           slots_qs = device.slot_set.all()
           if slots_qs.exists():
               for slot in slots_qs:
                   weight = params.get(str(count), None)
                   if weight:
                       slot.content_weight = weight
                   slot.save()
                   count += 1
           success_msg = 'successful'
       else:
           success_msg = 'unsuccessful'

       return HttpResponse(success_msg, content_type='text/plain', status=200)

   return HttpResponse("Method Not allowed", content_type='text/plain', status=405)


def set_device_active_view(request):
    if request.method == 'GET':
        device_id = request.GET.get('device_id',None)
        device = Device.objects.filter(device_id=device_id).first()
        print(device)
        if device:
            device.active = True
            device.save()
        return HttpResponse("successfull", status=200)

    return HttpResponse("Error", status=405)


