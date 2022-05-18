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

def get_views_array(model):
    much = []
    for i in model:
        much.append(i.total()) 
    return much

def get_error_messages(request, form):
    error_msg = form.errors.as_text().replace("*","").splitlines()
    for i in range(len(error_msg)):
        if i%2 != 0:
            messages.error(request, error_msg[i])