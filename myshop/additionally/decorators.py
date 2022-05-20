from myshop.models import Rating
from rest_framework.response import Response
from django.db.models import Avg

def incorrect_number(foo,):

    def wrapper(self, request, *args, **kwargs):
        if int(request.data.get('rating'))>5 or int(request.data.get('rating'))<0:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['rating'] = 5
            request.data._mutable = _mutable
            product = request.data['product']
            return Response({"average_rating":Rating.objects.filter(product = product).aggregate(avg = Avg('rating'))["avg"], 'del':False})
        return foo(self, request, *args, **kwargs)

    return wrapper