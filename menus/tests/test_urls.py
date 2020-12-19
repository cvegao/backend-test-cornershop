from django.test import SimpleTestCase
from django.urls import reverse, resolve

from menus.views import *


class TestUrls(SimpleTestCase):

    def test_staff_home_url_resolves(self):
        url = reverse('staff_home')
        self.assertEquals(resolve(url).func, staff_home)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_method)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_method)

    def test_staff_menus_resolves(self):
        url = reverse('staff_menus')
        self.assertEquals(resolve(url).func, staff_menus)

    def test_edit_menu_resolves(self):
        url = reverse('edit_menu', args=['1'])
        self.assertEquals(resolve(url).func, edit_menu)

    def test_delete_menu_resolves(self):
        url = reverse('delete_menu', args=['1'])
        self.assertEquals(resolve(url).func, delete_menu)

    def test_orders_resolves(self):
        url = reverse('orders')
        self.assertEquals(resolve(url).func, show_orders)

    def test_slack_resolves(self):
        url = reverse('slack')
        self.assertEquals(resolve(url).func, slack_notification)
