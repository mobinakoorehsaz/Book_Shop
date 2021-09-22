from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import CreateView, ListView
from products.models import *
from order.models import OrderItem, Order
from products.forms import SearchForm


# Create your views here.

# ---------------------ثبت نام-------------------------
class UserRegister(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('account:user_address')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return redirect('account:user_address')


# ------------------ ثبت آدرس هنگام ثبت نام---------------------
def user_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            address = Address.objects.create(user_id=request.user.id, txt=data['txt'],
                                             country=data['country'],
                                             city=data['city'], phone=data['phone'],
                                             postal_code=data['postal_code'])
            address.save()
            return redirect("products:index")
    form = AddressForm()
    return render(request, 'address/add_address.html', {'form': form})


# --------------------------ورود----------------------------
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['email'], password=data['password'])
            print(data)
            if user is not None:
                login(request, user)
                return redirect("products:index")
            else:
                messages.info(request, 'رمزعبور یا ایمیل اشتباهه', 'danger')
                return render(request, 'login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})


# ------------------------------- خروج----------------------------------
def user_logout(request):
    logout(request)
    messages.info(request, "با موفقیت خارج شدید", "danger")
    return redirect("products:index")


# --------------------------پنل کارمندان-----------------------------
class StaffPanel(ListView):
    model = Book
    template_name = 'staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all().order_by('created_at')
        context['categories'] = Category.objects.all()
        context['form'] = SearchForm()
        context['orders'] = Order.objects.all()
        return context


# ----------------------------- پروفایل کاربران----------------------------------
@login_required(login_url='account:user_login')
def user_profile(request):
    form = SearchForm()
    profile = Address.objects.filter(user_id=request.user.id)
    return render(request, 'profile.html', {'profile': profile, 'form': form})


def dashboard(request):
    admin = 0
    superuser = 0
    customer = 0
    users = User.objects.all()
    for user in users:
        if user.is_superuser:
            superuser += 1
        elif user.is_admin:
            admin = +1
        else:
            customer += 1

    orders = Order.objects.all().count()

    book = Book.objects.all()
    form = SearchForm()
    return render(request, 'dashbord.html',
                  {'book': book, 'form': form, 'users': users, 'customer': customer, 'admin': admin,'orders':orders})


# --------------------------اضافه کردن آدرس در پروفایل--------------------------
@login_required(login_url='account:user_login')
def user_add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_address = Address.objects.create(user_id=request.user.id, txt=data['txt'],
                                                  country=data['country'],
                                                  city=data['city'], phone=data['phone'],
                                                  postal_code=data['postal_code'])
            user_address.save()
            return redirect("account:user_profile")
    form = AddressForm()
    return render(request, 'address/add_address.html', {'form': form})


# ---------------------------حذف آدرس---------------------------------------
@login_required(login_url='account:user_login')
def remove_address(request, address_id):
    url = request.META.get('HTTP_REFERER')

    addresses = Address.objects.filter(user__email=request.user.email)
    x = addresses.count()
    if x < 2:
        messages.info(request, "!نمیخوام", "danger")
    else:
        Address.objects.filter(id=address_id).delete()
    return redirect(url)


# ----------------------------حذف کتاب -------------------------------
def remove_book(request, id):
    url = request.META.get('HTTP_REFERER')
    Book.objects.filter(id=id).delete()
    return redirect(url)


# -----------------------------حذف دسته بندی-----------------------
def remove_ctg(request, id):
    url = request.META.get('HTTP_REFERER')
    Category.objects.filter(id=id).delete()
    return redirect(url)


# -----------------------------ویرایش پروفایل---------------------------
@login_required(login_url='account:user_login')
def user_profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(email=request.user.email)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.username = data['username']
            user.save()
            return redirect('account:user_profile')
        else:
            return HttpResponse("valid nist")
    else:
        user_form = UserUpdateForm(instance=request.user)
        context = {'user_form': user_form}
        return render(request, 'update_profile.html', context)


# ------------------- forget password------------------------
class ResetPassword(PasswordResetView):
    template_name = 'forget_pass/reset.html'
    success_url = reverse_lazy('account:reset_done')
    email_template_name = 'forget_pass/link.html'


class DonePassword(PasswordResetDoneView):
    template_name = 'forget_pass/done.html'


class ConfirmPassword(PasswordResetConfirmView):
    template_name = 'forget_pass/confirm.html'
    success_url = reverse_lazy('account:complete')


class Complete(PasswordResetCompleteView):
    template_name = 'forget_pass/complete.html'


# --------------------------تاریخچه سفارشات----------------------------
@login_required(login_url='account:user_login')
def history(request):
    data = OrderItem.objects.filter(user_id=request.user.id)
    return render(request, 'history.html', {'data': data})
