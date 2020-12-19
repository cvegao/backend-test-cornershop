from sqlite3.dbapi2 import Date
from unittest import TestCase

from menus.forms import MenuForm, OptionForm
from menus.models import Menu


class TestForms(TestCase):

    def setUp(self):
        self.menu1 = Menu.objects.create(
            date=Date.today()
        )

    def test_menu_form_valid_data(self):
        form = MenuForm(data={
            'date': Date.today()
        })

        self.assertTrue(form.is_valid())

    def test_menu_form_no_data(self):
        form = MenuForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_option_form_valid_data(self):
        form = OptionForm(data={
            'content': 'content'
        })

        self.assertTrue(form.is_valid())

    def test_option_form_no_data(self):
        form = OptionForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
