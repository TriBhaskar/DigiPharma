from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name="home"),
    path('register/',views.registerPage, name="register"),
      path('login/',views.loginPage, name="login"),
      path('logout/',views.logoutUser, name="logout"),
    path('shop/',views.shop, name="shop"),
    path('shop_detail/',views.shoppingDetail, name="shop_detail"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),

]