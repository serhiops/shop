from inspect import _void
from myshop.models import Rating, CustomUser
from rest_framework.response import Response
from django.db.models import Avg
from config.main_config import REACT
from functools import wraps
import logging


def incorrect_number(cnumbers_max:int, cnumbers_min:int, level:logging = logging.DEBUG)->_void:
    """ Checks the correctness of entered data: max and min values of rating """
    def decorate(foo):
        log = logging.getLogger(foo.__module__)
        logmsg = foo.__name__
        @wraps(foo)
        def wrapper(self, request, *args, **kwargs):
            log.log(level, logmsg)
            if int(request.data.get('rating'))>cnumbers_max or int(request.data.get('rating'))<cnumbers_min:
                product = request.data['product']
                return Response({"average_rating":Rating.objects.filter(product = product).aggregate(avg = Avg('rating'))["avg"], 'del':False})
            return foo(self, request, *args, **kwargs)
        return wrapper
    return decorate
            


def currentUser(foo):
    """ Set current user for tests or react-coding """
    def wrapper(self, request, *args, **kwargs):
        if REACT:
            request.user = CustomUser.objects.get(pk = 1)
        return foo(self, request, *args, **kwargs)
    return wrapper
