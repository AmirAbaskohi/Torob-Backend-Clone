import string
import random
from .models import Product

def generate_uuid(length=12):
    uuids = set(Product.objects.values_list('uuid', flat=True))
    generated_uuid = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))
    while generated_uuid in uuids:
        generated_uuid = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))
    return generated_uuid