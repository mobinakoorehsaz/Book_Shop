from django.test import TestCase

# Create your tests here.
from .forms import *


class FormTests(TestCase):
    def test_forms(self):
        form_data = {'quantity': 1}
        form = ShoppingBasketForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'first_name': 'mobina', 'last_name': 'amini', 'address': 'ahvaz'}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'code': 2}
        form = CouponForm(data=form_data)
        self.assertTrue(form.is_valid())