from django.contrib import admin
from .models import Product, CustomUser, FavoriteProducts, Coments, Category, Ip, Ordering, Mark, Photo
from .forms import CustomUserCreationForm,ChangeEmail
from django.contrib.auth.admin import UserAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'price','category','salesman', 'created', 'updated', 'is_active')
    list_display_links = ('name',"id")
    search_fields = ('name', 'id')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'category')
    prepopulated_fields = {"slug": ("name",)}

class FavoriteProductsAdmin(admin.ModelAdmin):
    list_display = ("id","product","added")
    list_display_links = ('product',)
    search_fields = ("product","added")
    list_filter = ('added',)

class ComentsAdmin(admin.ModelAdmin):
    list_display = ("id","author","created","updated","is_active")
    list_display_links = ('author',"id")
    search_fields = ("author","created","id")
    list_filter = ('is_active',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    list_display_links = ('name',"id")
    search_fields = ("name","id")
    list_filter = ('id',"name")
    prepopulated_fields = {"slug": ("name",)}

class CustomUserAdmin(UserAdmin):
    form = ChangeEmail
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username',]

class OrderingAdmin(admin.ModelAdmin):
    list_display = ("id","product")


admin.site.register(Ordering, OrderingAdmin)
admin.site.register(CustomUser)
admin.site.register(Product, ProductAdmin)
admin.site.register(FavoriteProducts, FavoriteProductsAdmin)
admin.site.register(Coments, ComentsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ip)
admin.site.register(Mark)
admin.site.register(Photo)