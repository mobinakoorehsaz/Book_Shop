from django.contrib import admin
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'price', 'qty', 'discount', 'cash_discount', 'total_price','total_like']


admin.site.register(Book, ProductAdmin)
admin.site.register(Category)
admin.site.register(Chart)
