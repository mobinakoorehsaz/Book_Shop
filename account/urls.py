from django.urls import path

from . import views
from .views import *

app_name = 'account'
urlpatterns = [
    # ثبت نام
    path('register/', UserRegister.as_view(), name='user_register'),
    # اضافه کردن آدرس هنگام ثبت نام
    path('address/', views.user_address, name='user_address'),
    # ورود
    path('login/', views.user_login, name='user_login'),
    # خروج
    path('logout/', views.user_logout, name='user_logout'),
    # پروفایل
    path('profile/', views.user_profile, name='user_profile'),
    # اضافه کردن آدرس
    path('address/add/', views.user_add_address, name='add_address'),
    # پنل کارمندان
    path('staff/', StaffPanel.as_view(), name='staff_panel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # ویرایش پروفایل
    path('profile/update/', views.user_profile_update, name='user_profile_update'),
    # حذف آدرس
    path('address/delete/<int:address_id>/', views.remove_address, name='delete_address'),
    path('book/delete/<int:id>/', views.remove_book, name='delete_book'),
    path('category/delete/<int:id>/', views.remove_ctg, name='delete_ctg'),
    # forget pass
    path('reset/', ResetPassword.as_view(), name='reset_password'),
    path('reset/done/', DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', Complete.as_view(), name='complete'),
    # history
    path('history/', views.history, name='history'),

]
