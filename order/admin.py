from django.contrib import admin
from .models import *


# اردر آیتم ها بصورت جدول در اردر نشان داده میشوند
class ItemInLine(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'book', 'price', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'status', 'create']
    inlines = [ItemInLine]


class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'discount', 'active']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'price', 'quantity']


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShoppingBasket, ShoppingBasketAdmin)
admin.site.register(Coupon, CouponAdmin)
