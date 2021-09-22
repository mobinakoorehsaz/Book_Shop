from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import SearchForm
from order.forms import *
import emoji


# -------------------- اضافه کردن کتاب-------------------------
class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'description', 'price', 'category', 'qty']
    template_name = 'add_book.html'

    def get_success_url(self):
        return reverse('account:staff_panel')


# ----------------اضافه کردن دسته بندی--------------------
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'add_ctg.html'

    def get_success_url(self):
        return reverse('account:staff_panel')


# ----------------------صفحه اصلی ----------------------
class Index(ListView):
    model = Book
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = SearchForm()
        return context


# ---------------------جزئیات محصولات---------------------
class BookDetail(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShoppingBasketForm()
        context['categories'] = Category.objects.all()
        return context


# ---------------------search bar -----------------------
def product_search(request):
    books = Book.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data is not None:
                books = books.filter(Q(title=data) | Q(author=data))
            count = books.count()
            return render(request, 'search_response.html', {'books': books, 'form': form, 'count': count})


# # -----------------جزئیات هر دسته بندی-------------------------
class CategoryTasks(ListView):
    model = Book
    template_name = 'index.html'

    def get_queryset(self):
        return Book.objects.filter(category__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_queryset()
        context['categories'] = Category.objects.all()
        context['form'] = SearchForm()

        return context


# ------------------------- like , dislike --------------------------------
@login_required(login_url='account:user_login')
def like(request, id):
    book = get_object_or_404(Book, id=id)
    if book.like.filter(id=request.user.id).exists():
        book.like.remove(request.user)
    else:
        book.like.add(request.user)
        messages.success(request,
                         emoji.emojize(":red_heart: مرسی که لایک کردی.تو خودت لایکی :red_heart:", variant="emoji_type"),
                         'danger')
    return redirect('products:book_detail', book.id)
