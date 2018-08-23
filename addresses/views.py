from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

from django.utils.http import is_safe_url
# Create your views here.
from .models import Address,Contact
from devices.models import Device
from .forms import AddressForm,ContactForm


#/register/address/
def regiteration_view(request):
    form_type = request.POST.get("form_type",None)

    if form_type == 'address':
        form = AddressForm(request.POST or None)
    elif form_type == 'contact':
        form = ContactForm(request.POST or None)
    else:
        form = None
        return redirect('home')

    device_id_post = request.POST.get('device_id')
    device_id_get = request.GET.get('device_id')
    device_id = device_id_get or device_id_post or None

    next      = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next or next_post or None

    dev = get_object_or_404(Device, pk=int(device_id))

    if form.is_valid():
        instance = form.save(commit=False)
        instance.device = dev
        instance.save()
        flag = dev.set_active()

        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/home/")

    context = { "form": form, 'next_url': redirect_path }

    return HttpResponse("what?!")


