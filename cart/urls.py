from django.urls import path
from .views import (
    CartView,
    add_to_cart,
    decreaseCart,
    remove_from_cart,
)
app_name = 'mainapp'
urlpatterns = [
    path('cart/', CartView, name='cart-home'),
    path('cart/<slug>', add_to_cart, name='cart'),
    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    path('remove/<slug>', remove_from_cart, name='remove-cart'),

]
