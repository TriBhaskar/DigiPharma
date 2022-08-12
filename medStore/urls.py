from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name="home"),
    path('register/',views.registerPage, name="register"),
    path('shop/',views.shop, name="shop"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),

]