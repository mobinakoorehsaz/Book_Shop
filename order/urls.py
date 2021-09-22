from django.urls import path

from . import views
from .views import *

app_name = 'order'
urlpatterns = [
    # جزئیات سبد خرید
    path('', views.cart_detail, name='cart_detail'),
    # اضافه کردن
    path('add/<int:id>/', views.add_cart, name='add_card'),
    # حذف کردن
    path('remove/<int:id>/', views.remove_cart, name='remove_card'),
    # ساخت سفارش
    path('create/', views.order_create, name='order_create'),
    path('order_items/', OrderItemsList.as_view(), name='order_items'),
    path('order_detail/<int:id>/', views.order_detail, name='order_detail'),

]
