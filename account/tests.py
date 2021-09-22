from django.test import TestCase

# Create your tests here.
from .forms import *


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='mobina123', first_name='mobina', last_name='amini', email='mobina@gmail.com')

    def test_username_label(self):
        username = User.objects.get(id=1)
        field_label = username._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'نام کاربری')

    def test_first_name_label(self):
        first_name = User.objects.get(id=1)
        field_label = first_name._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'اسم')

    def test_last_name_label(self):
        last_name = User.objects.get(id=1)
        field_label = last_name._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'فامیل')

    def test_email_label(self):
        email = User.objects.get(id=1)
        field_label = email._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'ایمیل')


class FormTests(TestCase):
    def test_forms(self):
        form_data = {'email': 'mobina@gmail.com', 'username': 'mobina', 'first_name': 'mobina', 'last_name': 'kooresaz'}
        form = UserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'email': 'mobina@gmail.com', 'password': 'sadaldfksfhh'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'txt': 'padad', 'country': 'iran', 'city': 'ahvaz', 'phone': 123, 'postal_code': 12321}
        form = AddressForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'username': 'mobina123', 'first_name': 'mobina', 'last_name': 'kooresaz'}
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'txt': 'padad', 'country': 'iran', 'city': 'ahvaz', 'phone': 123, 'postal_code': 321}
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
