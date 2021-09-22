from django import forms
from .models import *


# برای جلوگیری از بوجود اومدن آیتم مشابه جدید در سبدخرید
class ShoppingBasketForm(forms.ModelForm):
    class Meta:
        model = ShoppingBasket
        fields = ['quantity']


# مشخصات سفارش
class OrderForm(forms.Form):
    # choice = forms.ModelChoiceField(queryset=Address.objects.filter())
    txt = forms.CharField()
    country = forms.CharField()
    city = forms.CharField()
    postal_code = forms.IntegerField()
    phone = forms.IntegerField()
    # def __init__(self, user, *args, **kwargs):
    #     super(OrderForm, self).__init__(*args, **kwargs)
    #     self.fields['address'] = forms.ModelChoiceField(
    #         queryset=Address.objects.filter(user_id=user.id))


# کد تخفیف
class CouponForm(forms.Form):
    code = forms.CharField(max_length=100)
