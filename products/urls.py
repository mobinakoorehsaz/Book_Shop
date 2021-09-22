from django.template.defaulttags import url
from django.urls import path, include
from .views import *
from . import views

app_name = 'products'
urlpatterns = [
    # صفحه اصلی
    path('', Index.as_view(), name='index'),
    # سرچ بار
    path('search/', views.product_search, name='product_search'),
    # جزئیات محصولات
    path('book/<int:pk>/', BookDetail.as_view(), name='book_detail'),
    # جزئیات  هر دسته بندی
    path('categories/<int:pk>/', CategoryTasks.as_view(), name='categoryTasks'),
    # اضافه کردن کتاب
    path('book/add/', BookCreateView.as_view(), name='adding_book'),
    # اضافه کردن دسته بندی
    path('category/add/', CategoryCreateView.as_view(), name='adding_ctg'),
    path('like/<int:id>/', views.like, name='like'),

]
