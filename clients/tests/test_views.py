import uuid
from datetime import datetime

from django.test import TestCase
from django.test import Client as Client_test
from django.urls import reverse

from clients.models import Order, Client
from menus.models import Menu, Option


class TestViews(TestCase):

    def setUp(self):
        self.client = Client_test()

    def test_client_home_GET(self):
        response = self.client.get(reverse('client_home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/clients_home.html')

    def test_client_home_POST_adds_new_order(self):
        menu = Menu(
            date=datetime.today(),
            unique_id=uuid.uuid4()
        )
        menu.save()
        option = Option(content='content')
        option.menu = menu
        option.save()
        client = Client()
        client.save()
        order = Order(
            client=client,
            option=option,
            comments='None'
        )
        order.save()

        record = Order.objects.get(pk=order.id)
        self.assertEquals(record, order)
