from django.urls import path
from rest_framework_nested import routers
from . import views

from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductVewSet,basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts',views.CartViewSet,basename='carts')

product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('review',views.ReviewViewSet,basename='product-review-data')

carts_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')





urlpatterns = router.urls + product_router.urls + carts_router.urls
# urlpatterns = [
#    path('products/',views.ProductsList.as_view()),
#    path('products/<int:pk>/',views.ProductDetail.as_view
#         ()),
#    path('collections/',views.CollectionList.as_view()),
#    path('collections/<int:pk>/',views.CollectionDetail.as_view())
# ]