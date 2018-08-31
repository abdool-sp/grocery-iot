from django.db import models
from django.db.models.signals import pre_save,post_save


from projectg.utils import unique_id_generator,get_index_queryset,set_device_active

# Create your models here.
DEV_TYPES = (
    ('A','TYPE A'),
    ('B', 'Type B')
)


class Device(models.Model):
    device_id   =   models.CharField(max_length=30,blank=True,null=True)
    dev_type    =   models.CharField(max_length=10, choices=DEV_TYPES)
    mfdate      =   models.DateTimeField(auto_now_add=True)
    #customer    =   models.ForeignKey(Customer,null=True,blank=True)
    active      =   models.BooleanField(default=False)


    def has_related_object(self):
        has_address = False
        has_contact = False
        try:
            has_address = self.address is not None
        except:
            pass
        try:
            has_contact = self.contact is not None
        except:
            pass

        return has_address,has_contact

    def get_address_and_contact(self):
        has_address, has_contact = self.has_related_object()

        if has_address and has_contact:
            address = self.address
            contact = self.contact
            return address,contact
        else:
            return None,"Not all"

    def set_active(self):
        has_address, has_contact = self.has_related_object()
        if has_contact and has_address:
            active = set_device_active(self.device_id)
            self.save()
        return self.active

    def __str__(self):
        return self.device_id

    def get_no_of_slots(self):
        obj = {
            'A': 2,
            'B': 3,
        }
        return obj[self.dev_type]

    def slot_grocery(self):
        slots = self.slot_set.all()
        if slots.exists():
            for slot in slots:
                if not slot.has_grocery():
                    return False

        return True


class Slot(models.Model):
    device              =   models.ForeignKey(Device,on_delete=models.CASCADE)
    slot_number         =   models.CharField(max_length=2,blank=True,null=True)
    grocery_name        =   models.CharField(max_length=100, blank=False, null=False)
    content_weight      =   models.DecimalField(decimal_places=1,max_digits=3,default=0.0)
    timestamp           =   models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.device.device_id, self.slot_number)

    def has_grocery(self):
        if self.grocery_name:
            return True
        return False





def post_save_slot_reciever(sender,instance,created, *args, **kwargs):
    if created:
        instance.slot_number = get_index_queryset(instance)
        instance.save()


def pre_save_device_reciever(sender,instance, *args, **kwargs):
    if not instance.device_id:
        generated_id = unique_id_generator(instance)
        instance.device_id = generated_id

def post_save_device_reciever(sender,instance,created, *args, **kwargs):
    if created:
        no = instance.get_no_of_slots()
        for i in range(no):
            slot = Slot.objects.create(device = instance)


pre_save.connect(pre_save_device_reciever,sender=Device)
post_save.connect(post_save_slot_reciever,sender=Slot)
post_save.connect(post_save_device_reciever,sender=Device)