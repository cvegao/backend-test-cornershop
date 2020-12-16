from datetime import datetime

from django.db import models

from menus.models import Option


class Client(models.Model):
    """Defines Client object. A client corresponds to a person ordering lunch"""
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    """Defines Order object. An order corresponds to a choice of menu"""
    date = models.DateTimeField(default=datetime.today)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=0)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, default=0)
    comments = models.CharField(max_length=250)
