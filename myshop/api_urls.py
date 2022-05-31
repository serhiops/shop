from django.urls import path, include
from . import api
from rest_framework import routers

routerUser = routers.SimpleRouter()
routerFavoriteProducts = routers.SimpleRouter()
routerPhoto = routers.SimpleRouter()

routerUser.register(r'user', api.UserViewset)
routerFavoriteProducts.register(r'favoriteProducts', api.FavoriteProductsViewset)
routerPhoto.register(r'photo', api.PhotoApi)

urlpatterns = [
    path("api/v1/product/<int:pk>/", api.ProductDetail.as_view()),
    path("api/v1/product/", api.ProductAPIList.as_view(), name = 'product-list-api'),
    path("api/v1/", include(routerUser.urls)),
    path("api/v1/", include(routerFavoriteProducts.urls)),
    path("api/v1/current_user/", api.CurrentUser.as_view()),
    path("api/v1/get_mark/<int:pk>/", api.GetMarksAPI.as_view()),
    path("api/v1/react/<int:pk>/", api.ReactAPI.as_view(), name='detail-product-api'),
    path('api/v1/react-mark/', api.ReactRatingApi.as_view(), name = 'rating-api'),
    path('api/v1/', include(routerPhoto.urls)),
    path('api/v1/add-to-cart/', api.AddToCart.as_view()),
    path('api/v1/coment/', api.CreateComentApi.as_view(), name = 'coment-list-api'),
    path('api/v1/coment/<int:pk>/', api.CreateComentApi.as_view(), name = 'detail-coment'),
    path('api/v1/create-ordering/', api.CreateOrdering.as_view()),
    path('api/v1/ordering/', api.OrderingDataApi.as_view())
]