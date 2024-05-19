from django.urls import path
from . import views
from .views import product_detail, add_product, update_product, delete_product, add_to_cart, cart_detail, update_cart, checkout, remove_from_cart
urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
    path('update_product/<int:pk>/', update_product, name='update_product'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),
    path('product/<int:pk>/add_to_cart/', add_to_cart, name='add_to_cart'),  
    path('product/<int:pk>/remove_from_cart/', remove_from_cart, name='remove_from_cart'),  
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/update/<int:pk>/', update_cart, name='update_cart'),  
    path('checkout/', checkout, name='checkout'),  
]