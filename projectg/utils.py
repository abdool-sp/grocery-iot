from django.utils.text import slugify
import random,string,json
from paho.mqtt import publish

def set_device_active(device_id):
    topic = '/' + device_id +'/set_active'
    publish.single(topic,payload=json.dumps({'active':True}), hostname='iot.eclipse.org')
    return True



def random_string_gen(size=10,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_id_generator(instance):
    device_new_id = random_string_gen().upper()

    klass = instance.__class__
    qs_exist = klass.objects.filter(device_id=device_new_id).exists()
    if qs_exist:
        return unique_id_generator(instance)
    return device_new_id

DONT_USE = []
def unique_slug_generator(instance,new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug in DONT_USE:
        new_slug = "{slug}-{randstr}".format(slug=slug,
                                             randstr = random_string_gen(size=4)
                                             )
        return unique_slug_generator(instance,new_slug=new_slug)
    klass = instance.__class__
    qs_exist = klass.objects.filter(slug=slug).exists()
    if qs_exist:
        new_slug = "{slug}-{randstr}".format(slug=slug,
                                             randstr = random_string_gen(size=4)
                                             )
        return unique_slug_generator(instance,new_slug=new_slug)

    return slug

def get_index_queryset(instance):
    qs = instance.device.slot_set.all()
    temp = list()
    for q in qs:
        temp.append(q)
    index = str(temp.index(instance) + 1)
    return index
