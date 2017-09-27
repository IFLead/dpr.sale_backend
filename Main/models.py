from django.contrib.auth.models import User
from django.db import models

from filer.fields.image import FilerImageField


class Category(models.Model):
    name = models.CharField('Название', max_length=128)


RUB = 0
USD = 1
CURRENCIES = (
    (RUB, 'Рубль'),
    (USD, 'Доллар'),
)


class City(models.Model):
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class District(models.Model):
    city = models.ForeignKey(City, verbose_name="Город", null=True, blank=False)
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория')
    is_top = models.BooleanField('В топе')
    main_photo = models.ImageField('Главное изображение', upload_to='title_photos')
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    price = models.DecimalField('Стоимость', decimal_places=0, max_digits=9)
    currency = models.IntegerField('Валюта', choices=CURRENCIES)
    owner = models.ForeignKey(User, verbose_name='Владелец')
    verified = models.BooleanField('Подтвержден', default=False)
    closed = models.BooleanField('Закрыт', default=False)
    reason = models.TextField('Причина', null=True, blank=True)

    rooms = models.PositiveSmallIntegerField('Количество комнат', default=1)
    floor = models.PositiveSmallIntegerField('Этаж', default=1)
    square = models.FloatField('Площадь (метры кв.)', default=1)
    storeys = models.PositiveSmallIntegerField('Этажность здания', default=1)
    district = models.ForeignKey(District, verbose_name='Район')


class Image(models.Model):
    image_file = FilerImageField()
    obj = models.ForeignKey(Post, related_name='photos')


class CustomData(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', null=True, related_name='custom')
    type = models.IntegerField('Статус', )
    phone = models.CharField('Номер телефона', blank=True, max_length=25, null=True)  # 38 050 240 92 92
    email = models.EmailField('Электронная почта', blank=True, null=True)


    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Fastoran'
        verbose_name_plural = 'Fastoran'

