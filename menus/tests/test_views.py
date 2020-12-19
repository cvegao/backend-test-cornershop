import uuid
from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from menus.models import Menu, Option


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('user_test', 'usertest@mail.com', '123')

    def test_login(self):
        self.client.login(username='user_test', password='123')
        response = self.client.get(reverse('staff_home'))
        self.assertEquals(response.status_code, 200)

    def test_staff_home_GET(self):
        self.client.login(username='user_test', password='123')

        response = self.client.get(reverse('staff_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menus/staff_home.html')

    def test_staff_home_POST(self):
        menu = Menu(
            date=datetime.today(),
            unique_id=uuid.uuid4()
        )
        menu.save()
        option = Option(content='content')
        option.menu = menu
        option.save()

        record = Option.objects.get(pk=option.id)
        self.assertEquals(record, option)

    def test_staff_menus_GET(self):
        self.client.login(username='user_test', password='123')

        response = self.client.get(reverse('staff_menus'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menus/staff_menus.html')

    def test_slack_notification(self):
        self.client.login(username='user_test', password='123')

        menu = Menu(
            date=datetime.today(),
            unique_id=uuid.uuid4()
        )
        menu.save()
        option = Option(content='content')
        option.menu = menu
        option.save()

        response = self.client.get(reverse('slack'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menus/slack.html')
