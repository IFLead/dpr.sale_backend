from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=128)


class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория')
    # photo
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    price = models.DecimalField('Стоимость', decimal_places=0, max_digits=9)
    owner = models.ForeignKey(User, verbose_name='Владелец')
    verified = models.BooleanField('Подтвержден', default=False)
    closed = models.BooleanField('Закрыт', default=False)
    reason = models.TextField('Причина', null=True, blank=True)
