import random
from django.contrib import messages
def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_views_quantity(model):
    much = 0
    for i in model:
        much += i.total()
    return much

def get_max(model):
    max = 0
    for i in model:
        if i.total() > max:
            max = i.total()
    return max

def get_min(model):
    min = 100000000000
    for i in model:
        if i.total() < min:
            min = i.total()
    return min

def get_error_messages(request, form):
    error_msg = form.errors.as_text().replace("*","").splitlines()
    for i in range(len(error_msg)):
        if i%2 != 0:
            messages.error(request, error_msg[i])