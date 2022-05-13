from django.forms import ValidationError
from .models import CustomUser, Product, Mark, Coments, FavoriteProducts, Rating, PostOfices, Ordering, Photo
from . import serializers
from django.utils.text import slugify
from rest_framework import generics
#from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from django.db.models import Q, Avg
from config.main_config import REACT


class ProductAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["slug"] =slugify(serializer.initial_data["name"])
        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def update(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data["slug"] = slugify(request.data.get("name"))
        request.data._mutable = _mutable
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        product = Product.objects.get(pk = kwargs["pk"])
        product.is_active = not product.is_active
        product.save()
        return Response(serializers.ProductSerializer(product).data)

class MarkAPIListOrCreate(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = serializers.MarkSerializer

    def post(self, request, *args, **kwargs):
        try:
            mark = Mark.objects.get(product__id = request.data["product"], user__id = request.data["user"])
            if mark:
                mark.delete()
        except:
            pass
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        marks = Mark.objects.all()
        return Response({"marks":serializers.MarkSerializer(marks, many=True).data, "user":serializers.UserSerializer(request.user).data})

class MarkAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = serializers.MarkSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        mark = Mark.objects.get(product__id = request.data["product"], user__id = request.data["user"])
        
        like = request.data.get("like", False)
        dislike = request.data.get("dislike", False)
        
        if like == dislike:
            raise ValidationError("error! like == dislike")

        if like:
            if mark.dislike:
                mark.like = not mark.like
                mark.dislike = not mark.dislike
            elif mark.like:
                mark.delete()
        
        if dislike:
            if mark.like:
                mark.dislike = not mark.dislike
                mark.like = not mark.like
            elif mark.dislike:
                mark.delete()

        return super().put(request, *args, **kwargs)

class ComentViewset(ModelViewSet):
    queryset = Coments.objects.all()
    serializer_class = serializers.ComentsSerializer

    def list(self, request, *args, **kwargs):
        coments = Coments.objects.all()
        return Response({"coments":serializers.ComentsSerializer(coments,many=True).data, 
                        "current_user":serializers.UserSerializer(request.user).data})

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data["author"] = 1
        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

class UserViewset(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

class FavoriteProductsViewset(ModelViewSet):
    queryset = FavoriteProducts.objects.all()
    serializer_class = serializers.FavoriteProductsSerializer

class CurrentUser(views.APIView):
    def get(self, request):
        return Response({"user":serializers.UserSerializer(request.user).data})

class RatingViewset(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = serializers.RatingSerializer

class GetRatingAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        rating = Rating.objects.filter(product__id = kwargs.get("pk", None))
        return Response({"rating":serializers.RatingSerializer(rating, many = True).data, "user":serializers.UserSerializer(self.request.user).data})

class GetMarksAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = serializers.MarkSerializer

    def get(self, request, *args, **kwargs):
        marks = Mark.objects.filter(product__id = kwargs.get("pk", None))
        return Response({"marks":serializers.MarkSerializer(marks, many = True).data, "user":serializers.UserSerializer(self.request.user).data})

class GetComentAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coments.objects.all()
    serializer_class = serializers.ComentsSerializer

    def get(self, request, *args, **kwargs):
        coments = Coments.objects.filter(product__id = kwargs.get("pk", None))
        return Response({"coments":serializers.ComentsSerializer(coments, many = True).data, "user":serializers.UserSerializer(self.request.user).data})

class GetProductsFilter(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        city = self.request.query_params.get("city", False)
        begin_price = self.request.query_params.get("begin_price", 0)
        end_price = self.request.query_params.get("end_price", None)
        category = self.request.query_params.get("category", None)
        if not city:
            products = Product.objects.filter(Q(price__gte = begin_price)&Q(price__lte = end_price)&Q(category__slug = category)).count()
        else:
            products = Product.objects.filter(Q(price__gte = begin_price)&Q(price__lte = end_price)&Q(salesman__city = city)&Q(category__slug = category)).count()
        return Response(products)

class GetPostOficesList(generics.ListAPIView):
    queryset = PostOfices.objects.all()
    serializer_class = serializers.PostOficesSerializer

    def get(self, request, *args, **kwargs):
        city = self.request.query_params["city"]
        ofices = PostOfices.objects.filter(name__contains = city, is_active = True)
        return Response(serializers.PostOficesSerializer(ofices, many = True).data)

class GetOrderDataList(generics.ListAPIView):
    queryset = Ordering.objects.all()
    serializer_class = serializers.OrderingSerializer

    def get(self, request, *args, **kwargs):
        product_id = self.request.query_params["productID"]
        product = Product.objects.get(pk = product_id)
        salesman = CustomUser.objects.get(pk = product.salesman.id)
        return Response({"user":serializers.UserSerializer(self.request.user).data, "salesman":serializers.UserSerializer(salesman).data, "product":serializers.ProductSerializer(product).data})

class GetRatingMarksComentsList(generics.ListAPIView):
    queryset = Coments.objects.all()
    serializer_class = serializers.ComentsSerializer

    def get(self, request, *args, **kwargs):
        product_id = self.request.query_params["productID"]
        coments = Coments.objects.filter(product__id = product_id,is_active = True)
        marks = Mark.objects.filter(product__id = product_id)
        rating = Rating.objects.filter(product__id = product_id)
        return Response({"coments":serializers.ComentsSerializer(coments, many = True).data,
                        "marks":serializers.MarkSerializer(marks, many = True).data,
                        "rating":serializers.RatingSerializer(rating, many = True).data,
                        "user":serializers.UserSerializer(self.request.user).data})

class ReactAPI(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk = kwargs["pk"])
        image =serializers.PhotoSerializer(product.photos.all(), many = True).data
        coments = Coments.objects.filter(product = product)
        rating = Rating.objects.filter(product = product)
        likes = Mark.objects.filter(product = product, like = True)
        dislikes = Mark.objects.filter(product = product, dislike = True)
        if request.user.id == None:
            return Response({
                'product':serializers.ProductSerializer(product).data, 
                'likes':likes.count(),
                'dislikes': dislikes.count(), 
                'current_user': False,
                "coments":serializers.ComentsSerializer(coments, many = True).data,
                'company_name':product.salesman.company,
                'images':image
            })
        if REACT:
            current_user = CustomUser.objects.get(pk = 1)
        else:
            current_user = self.request.user
        is_liked_by_current_user = likes.filter(user = current_user).count()
        is_disliked_by_current_user = dislikes.filter(user = current_user).count()
        try:
            current_user_rating = serializers.RatingSerializer(rating.get(user = current_user)).data
        except:
            current_user_rating = False
        if Ordering.objects.filter(user = current_user, product = product):
            is_bought = True
        else:
            is_bought = False
        return Response({'product':serializers.ProductSerializer(product).data, 
                        'likes':likes.count(),
                        'dislikes': dislikes.count(), 
                        'current_user': serializers.UserSerializer(current_user).data,
                        "is_liked_by_current_user":bool(is_liked_by_current_user),
                        "is_disliked_by_current_user":bool(is_disliked_by_current_user),
                        "coments":serializers.ComentsSerializer(coments, many = True).data,
                        "rating":serializers.RatingSerializer(rating, many = True).data,
                        "current_user_rating":current_user_rating,
                        "average_rating": rating.aggregate(avg = Avg('rating'))['avg'],
                        'images':image,
                        'is_bought':is_bought,
                        'company_name':product.salesman.company})

class ReactAPIPost(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = serializers.MarkSerializer

    def post(self, request, *args, **kwargs):
        if REACT:
            user = CustomUser.objects.get(pk = 1)
        else:
            user = self.request.user
        product = Product.objects.get(pk = request.data["product"])
        if request.data.get('like', False):
            mark, created = Mark.objects.get_or_create(product = product, user = user)
            if not created and mark.like == True:
                mark.delete()
                return Response({"delete":True})
            elif mark.dislike:
                mark.dislike = False
                mark.like = True
            else:
                mark.like = True
            mark.save(update_fields=['like', 'dislike'])
        elif request.data.get('dislike', False):
            mark, created = Mark.objects.get_or_create(product = product, user = user)
            if not created and mark.dislike == True:
                mark.delete()
                return Response({"delete":True})
            elif mark.like:
                mark.like = False
                mark.dislike = True
            else:
                mark.dislike = True
            mark.save(update_fields=['like', 'dislike'])
        return Response(serializers.MarkSerializer(mark).data)

class ReactMarkApi(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = serializers.RatingSerializer

    def post(self, request, *args, **kwargs):
        if REACT:
            user = CustomUser.objects.get(pk = 1)
        else:
            user = self.request.user 
        product = Product.objects.get(pk = request.data["product"])
        rating,created = Rating.objects.get_or_create(user = user,product = product )
        if not created and rating.rating == int(request.data.get('rating', False)):
            rating.delete()
            return Response({"average_rating":Rating.objects.filter(product = product).aggregate(avg = Avg('rating'))["avg"], 'del':True})
        else:
            rating.rating = int(request.data["rating"])
            rating.save(update_fields=['rating'])
        return Response({"average_rating":Rating.objects.filter(product = product).aggregate(avg = Avg('rating'))["avg"], 'del':False})

class PhotoApi(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer

""" class ProductAPI(views.APIView):
    def get(self, request):
        products = Product.objects.filter(is_active = True)
        return Response({"products":ProductSerializer(products, many = True).data})

    def post(self, request):
        request.data["slug"] =slugify(request.data["name"])
        
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success add":serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", False)

        if not pk:
            return Response({"error": "pk doesn't exists!"})
        else:
            product = Product.objects.get(pk=pk)
        try:
            product.delete()
            return Response({"success delete": f"{product}"})
        except Exception as _ex:
            return Response({"error": f"{_ex}"})

    def put(self, request, *args, **kwargs):
        request.data["slug"] =slugify(request.data["name"])
        pk = kwargs.get("pk", False)
        if pk:
            product = Product.objects.get(pk = pk)
        else:
            return Response({"error":"No such pk!"})
        try:
            serializer = ProductSerializer(data=request.data, instance=product)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success update":serializer.data})
        except Exception as _ex:
            return Response({"error":f"{_ex}"}) """


""" class ProductViewset(ModelViewSet):
    queryset = Product.objects.filter(is_active = True)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["slug"] =slugify(serializer.initial_data["name"])
        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data["slug"] = slugify(request.data.get("name"))
        request.data._mutable = _mutable
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def categories(self, request):
        cats = Category.objects.all()
        return Response({"categories":[c.name for c in cats]})   """