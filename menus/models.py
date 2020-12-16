import uuid

from django.db import models


class Menu(models.Model):
    """Defines Menu object"""
    date = models.DateField()
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['date']

    def join(self):
        """Joins the date, UUID and the option of an specific date (menu's date)"""
        return {self.date: Option.objects.filter(menu=self).values('content')}


class Option(models.Model):
    """Defines Option object. An option corresponds to a menu's option"""
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, default=0)
    content = models.CharField(max_length=250)

    def __str__(self):
        return self.content
