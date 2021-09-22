from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.urls import reverse


# دسته بندی
class Category(models.Model):
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسنه بندی ها"

    name = models.CharField(max_length=200, verbose_name='نام')

    def __str__(self):
        return self.name


# کتاب
class Book(models.Model):
    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب ها"

    # موضوع کتاب
    title = models.CharField(max_length=200, verbose_name='موضوع')
    # نویسنده
    author = models.CharField(max_length=200, verbose_name='نویسنده')
    # شرح
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='شرح')
    # قیمت
    price = models.PositiveIntegerField(verbose_name='قیمت')
    # تعداد
    qty = models.IntegerField(verbose_name='موجودی انبار')
    # دسته بندی
    category = models.ManyToManyField(Category, max_length=200, verbose_name='دسته بندی')
    # تاریخ ثبت
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    update = models.DateTimeField(auto_now=True)
    # تخفیف
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف درصدی')
    cash_discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف نقدی')
    # قیمت ب تخفیف
    total_price = models.PositiveIntegerField()
    like = models.ManyToManyField('account.User', blank=True, related_name='like')
    dislike = models.ManyToManyField('account.User', blank=True, related_name='dislike')
    total_like = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def total_like(self):
        return self.like.count()

    @property
    def total_price(self):
        if self.cash_discount:
            return int(self.price - self.cash_discount)
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        else:
            return self.price

    def get_absolute_url(self):
        return reverse('products:book_detail', kwargs={'pk': self.pk})


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pr_update', blank=True, null=True)

    def __str__(self):
        return self.name

def product_post_saved(sender, instance,created,*args,**kwargs):
    data = instance
    Chart.objects.create(product=data, unit_price= data.unit_price, update=data.update,name=data.name)

post_save.connect(product_post_saved,sender=Book)