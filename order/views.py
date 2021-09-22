from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView

from products.forms import SearchForm
from .forms import *


# Create your views here.

# --------------------------------order----------------------------
@login_required(login_url='account:user_login')
def order_create(request):
    """
    ساخت و ثبت سفارش
    """
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart = ShoppingBasket.objects.filter(user_id=request.user.id)
            order = Order.objects.create(user_id=request.user.id, email=request.user.email,
                                         first_name=request.user.first_name,
                                         last_name=request.user.last_name, address=data['txt'], country=data['country'],
                                         city=data['city'], postal_code=data['postal_code'], phone=data['phone'])
            for item in cart:
                total = 0
                total += item.product.price * item.quantity
                OrderItem.objects.create(order_id=order.id, user_id=request.user.id,
                                         book_id=item.product.id, quantity=item.quantity)
                x = item.product.qty - item.quantity
                Book.objects.filter(id=item.product.id).update(qty=x)
            ShoppingBasket.objects.filter(user_id=request.user.id).delete()
            messages.info(request, 'سفارش شما ثبت شد', 'danger')
            return render(request, 'order.html', {'form': form})
    return render(request, 'order.html', {'form': form})


# --------------------shopping basket views -----------------------
@login_required(login_url='account:user_login')
def cart_detail(request):
    """
    جزئیات سبد خرید کاربر
    """
    form = SearchForm()
    quantity = ShoppingBasketForm()
    categories = Category.objects.all()
    cart = ShoppingBasket.objects.filter(user_id=request.user.id)
    items = ShoppingBasket.objects.filter(user_id=request.user.id).count()
    coupon_form = CouponForm()
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        time = timezone.now()
        if coupon_form.is_valid():
            code = coupon_form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'این کد وجود ندارد', 'danger')
                return redirect('order:cart_detail')
            total = 0
            for p in cart:
                total += p.product.price * p.quantity
                discount_price = (coupon.discount / 100) * total
                total = total - discount_price
            context = {'cart': cart, 'total': total, 'coupon_form': coupon_form, 'quantity': quantity, 'form': form}
            return render(request, 'shopping_basket.html', context)
    total = 0
    for p in cart:
        total += p.product.total_price * p.quantity
    context = {'cart': cart, 'total': total, 'coupon_form': coupon_form, 'items': items, 'categories': categories,
               'form': form
               }
    return render(request, 'shopping_basket.html', context)


@login_required(login_url='account:user_login')
def add_cart(request, id):
    """
    اضافه کردن کتاب به سبد خرید
    """
    data = ShoppingBasket.objects.filter(user_id=request.user.id, product_id=id)
    if data:
        check = 'yes'
    else:
        check = 'no'
    if request.method == 'POST':
        form = ShoppingBasketForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                shop = ShoppingBasket.objects.get(user_id=request.user.id, product_id=id)
                shop.quantity += info
                shop.save()
            else:
                ShoppingBasket.objects.create(user_id=request.user.id, product_id=id, quantity=info)
                return redirect("order:cart_detail")
    return redirect("order:cart_detail")


@login_required(login_url='account:user_login')
def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    ShoppingBasket.objects.filter(id=id).delete()
    return redirect(url)


class OrderItemsList(ListView):
    model = OrderItem
    template_name = 'order_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['form'] = SearchForm()
        return context


def order_detail(request, id):
    form = SearchForm()
    order_items = OrderItem.objects.filter(order_id=id)
    return render(request, 'order_detail.html', {'order_items': order_items,'form':form})
