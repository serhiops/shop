from django.urls import path
from .views import *
from . import api_urls

app_name = 'myshop'

urlpatterns = [
    path("by_category/<slug:cat_slug>/", ByCategory.as_view(), name = "by_category"),
    path("detail/<int:prod_pk>/<slug:prod_slug>/", ProductDetail.as_view(), name = "detail"),
    path("korzina/", FavoriteProductsList.as_view(), name = "favorite_products"),
    path("register/", Register.as_view(), name = "register"),
    path("register_salesman/", Register.as_view(), name = "register_salesman"),
    path("register_code/", register_code, name = "register_code"),
    path("login/", Login.as_view(), name = "login"), 
    path("logout/", user_logout, name = "logout"),
    path("user_profile/", user_profile, name = "user_profile"),
    path("change_email/", change_email, name = "change_email"),
    path("delete_favorite_product/<int:pk_fp>/", delete_fav_pr, name = "delete_fav_pr"),
    path("add_product/", AddProduct.as_view(), name = "add_product"),
    path("delete_product/<slug:slug_pr>/", set_unactive, name = "delete_product"),
    path("statistic/", statistic,name="statistic"),
    path("detail_statistic/<slug:slug_pr>/", detail_statistic, name = "detail_statistic"),
    path("", Index.as_view(), name = "index"),
    path("change_product/<slug:slug_pr>/", ChangeProduct.as_view(), name = "change_product"),
    path("ordering/<int:pk_sal>/<slug:slug_prod>/", ordering, name = "ordering"),
    path("user_orders/", user_orders, name = "user_orders"),
    path("set_done/<int:pk_ord>/", set_done, name = "set_done"),
    path("set_active/<slug:slug_prd>", set_active, name = "set_active"),
    path("backorders/", backorders, name = "backorders"),
    path("user_active_oders/", user_active_oders,name =  "user_active_oders"),
    path("completed_orders/", completed_orders, name = "completed_orders"),
    path("accepted_products/", accepted_products, name = 'accepted_products'),
    path("salesman/<slug:salesman_slug>/", salesman_profile, name = "salesman_profile"), 
    path("change_password/", ChangePassoword.as_view(), name = "change_password"),
    
    path("reset_password/", PasswordReset.as_view(), name = "password_reset"),
    path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirm.as_view(), name = 'password_reset_confirm'),
] + api_urls.urlpatterns
