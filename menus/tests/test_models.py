from sqlite3.dbapi2 import Date

from django.test import TestCase

from menus.models import Menu, Option


class TestModels(TestCase):
    def setUp(self):
        self.menu1 = Menu.objects.create(
            date=Date.today()
        )

    def test_join(self):
        Option.objects.create(
            menu=self.menu1,
            content='content'
        )

        join_object = {
            'id': self.menu1.id,
            'date': self.menu1.date,
            'options': Option.objects.filter(menu=self.menu1).values('content')
        }

        self.assertEquals(self.menu1.join(), join_object)
