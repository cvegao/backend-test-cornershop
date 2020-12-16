# Generated by Django 3.1.2 on 2020-12-15 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='options',
        ),
        migrations.AddField(
            model_name='option',
            name='menu',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='menus.menu'),
            preserve_default=False,
        ),
    ]
