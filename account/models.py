from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from .manager import *


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "کاربران"

    username = models.CharField(max_length=200, verbose_name='نام کاربری')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=100, verbose_name='اسم', null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name='فامیل', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Address(models.Model):
    class Meta:
        verbose_name = "نشانی"
        verbose_name_plural = "نشانی ها"

    txt = models.TextField(max_length=200, verbose_name='متن')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='کاربر')
    country = models.CharField(max_length=100,  verbose_name='کشور')
    city = models.CharField(max_length=100, verbose_name='شهر')
    postal_code = models.IntegerField( verbose_name='کد پستی')
    phone = models.IntegerField( verbose_name='تلفن')

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = 'پروفایل ها'

    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='کاربر')


def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=User)
