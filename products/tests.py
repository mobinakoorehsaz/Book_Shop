from django.test import TestCase
# Create your tests here.
from products.models import Book, Category
from .forms import SearchForm


class SimpleTest(TestCase):
    def test_index_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='mountains', author='Bob', price=20000, qty=2,
                            description='natural book about mountains')

    def test_title_label(self):
        title = Book.objects.get(id=1)
        field_label = title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'موضوع')

    def test_author_label(self):
        author = Book.objects.get(id=1)
        field_label = author._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'نویسنده')

    def test_price_label(self):
        price = Book.objects.get(id=1)
        field_label = price._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'قیمت')

    def test_qty_label(self):
        qty = Book.objects.get(id=1)
        field_label = qty._meta.get_field('qty').verbose_name
        self.assertEqual(field_label, 'موجودی انبار')

    def test_description_label(self):
        description = Book.objects.get(id=1)
        field_label = description._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'شرح')

    def test_title_max_length(self):
        title = Book.objects.get(id=1)
        max_length = title._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/book/1/')


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='ادبیات')

    def test_name_label(self):
        name = Category.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'نام')


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('your_server_ip:8000')
        self.assertEqual(response.status_code, 404)


class FormTests(TestCase):
    def test_forms(self):
        form_data = {'search': 'bob'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
