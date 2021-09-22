from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


# ------------------- ساخت یوزر و ثبت نام---------------------------
class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('password not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_password(self):
        return self.initial['password']


# ----------------------------ورود--------------------------
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        fields = ['email', 'password', ]


# ----------------------اضافه کردن آدرس---------------------
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['txt', 'country', 'city', 'phone', 'postal_code', ]


# --------------------------ویرایش پروفایل----------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['txt', 'country', 'city', 'phone', 'postal_code', ]
