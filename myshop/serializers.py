from rest_framework import serializers
from .models import Product, Mark, Coments, CustomUser, FavoriteProducts, Rating, Ordering, Photo

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"

class ComentsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(source='author.username' ,queryset=CustomUser.objects.all())
    class Meta:
        model = Coments
        fields = "__all__"

    def create(self, validated_data):
        delet = validated_data.get("author", False)
        validated_data["author"] = delet.get("username", False)
        validated_data['is_active'] = True
        return Coments.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = instance.author.username
        return response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        
class FavoriteProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProducts
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class OrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordering
        fields = "__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = ProductSerializer(instance.product).data
        response['salesman'] = UserSerializer(instance.salesman).data
        response['user'] = UserSerializer(instance.user).data
        return response

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__" 