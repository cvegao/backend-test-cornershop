from django.test import SimpleTestCase
from django.urls import reverse, resolve

from clients.views import client_home


class TestUrls(SimpleTestCase):

    def test_client_home_url_is_resolved(self):
        url = reverse('client_home')
        self.assertEquals(resolve(url).func, client_home)
