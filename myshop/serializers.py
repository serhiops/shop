from rest_framework import serializers
from .models import Product, Mark, Coments, CustomUser, FavoriteProducts, Rating, PostOfices, Ordering

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
        user = delet.get("username", False)
        del validated_data["author"]
        validated_data["author"] = user
        validated_data["is_active"] = True
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

class PostOficesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOfices
        fields = "__all__"

class OrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordering
        fields = "__all__" 