from sqlite3.dbapi2 import Date
from unittest import TestCase

from clients.forms import ClientForm, OrderForm
from menus.models import Menu, Option


class TestForms(TestCase):

    def setUp(self):
        self.menu1 = Menu.objects.create(
            date=Date.today()
        )

        self.option1 = Option.objects.create(
            menu=self.menu1,
            content='content'
        )

    def test_client_form_valid_data(self):
        form = ClientForm(data={
            'name': 'client1',
            'phone_number': '123'
        })

        self.assertTrue(form.is_valid())

    def test_client_form_no_data(self):
        form = ClientForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_order_form_valid_data(self):
        form = OrderForm(data={
            'menu': self.menu1,
            'option': self.option1,
            'comments': 'comment1'
        })

        self.assertTrue(form.is_valid())

    def test_order_form_no_data(self):
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
