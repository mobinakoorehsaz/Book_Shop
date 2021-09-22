from products.models import *
from account.models import *


# Create your models here.


# سبدخرید
class ShoppingBasket(models.Model):
    class Meta:
        verbose_name = "سبدخرید"
        verbose_name_plural = "سبدهای خرید"

    # سبد خرید مطعلق به چه کسی هست
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='basket_user', verbose_name='کاربر')
    # محصولاتی که کاربر به سبد اضافه کرده
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='product', verbose_name='محصول')
    # تعداد محوصلات
    quantity = models.PositiveIntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.user.email


# سفارشات
class Order(models.Model):
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='کاربر')
    create = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    status = models.BooleanField(default=False, verbose_name='وضعیت')
    email = models.EmailField(verbose_name='ایمیل')
    address = models.CharField(max_length=200, verbose_name='نشانی')
    first_name = models.CharField(max_length=200, verbose_name='اسم')
    last_name = models.CharField(max_length=200, verbose_name='فامیل')
    country = models.CharField(max_length=100, verbose_name='کشور')
    city = models.CharField(max_length=100, verbose_name='شهر')
    postal_code = models.IntegerField(verbose_name='کد پستی')
    phone = models.IntegerField(verbose_name='تلفن')

    def __str__(self):
        return self.user.username


# ریز سفارشات
class OrderItem(models.Model):
    class Meta:
        verbose_name = "آینم"
        verbose_name_plural = "ریز سفارشات"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item', verbose_name='سفارش')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='کاربر')
    book = models.ForeignKey('products.Book', on_delete=models.CASCADE, verbose_name='کتاب')
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.book.title

    @property
    def price(self):
        return self.book.total_price * self.quantity


class Coupon(models.Model):
    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف ها"

    code = models.CharField(max_length=100, unique=True, verbose_name='کد تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال')
    start = models.DateTimeField(verbose_name='شروع')
    end = models.DateTimeField(verbose_name='پایان')
    discount = models.IntegerField(verbose_name='مقدار')
