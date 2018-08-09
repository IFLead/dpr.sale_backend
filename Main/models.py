from django.contrib.auth.models import User
from django.db import models
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.db.models import F, Max


class Category(models.Model):
    name = models.CharField('Название', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# class MiniImage(models.Model):
#     name = models.CharField('Название', max_length=128)
#     main_photo = FilerImageField(verbose_name='Главное изображение', null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Пикча для теста'
#         verbose_name_plural = 'Пикчи для теста'
#
#     def __str__(self):
#         return self.name


class Currency(models.Model):
    name = models.CharField('Название', max_length=128)
    symbol = models.CharField('Символ', max_length=3)
    is_prefix = models.BooleanField('Префиксный символ', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class City(models.Model):
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class District(models.Model):
    city = models.ForeignKey(City, verbose_name="Город", null=True, blank=False, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class State(models.Model):
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'


class Material(models.Model):
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Window(models.Model):
    name = models.CharField('Название', max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Окно'
        verbose_name_plural = 'Окна'


# class Living_space(models.Model):
#     name = models.CharField('Тип', max_length=55)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Жилая площадь'
#         verbose_name_plural = 'Жилые площади'


class Client(models.Model):
    name = models.CharField('Имя', max_length=55)
    decription = models.TextField('Описание', max_length=256)
    phone_one = models.CharField('Первый номер телефона', blank=True, max_length=25, null=True)
    phone_two = models.CharField('Второй номер телефона', blank=True, max_length=25, null=True)
    phone_three = models.CharField('Третий номер телефона', blank=True, max_length=25, null=True)
    phone_four = models.CharField('Четвёртый номер телефона', blank=True, max_length=25, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class TreeCategory(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        # if self.is_leaf_node():
        return self.get_level() * '-' + self.name

    class Meta:
        verbose_name = 'Тип недвижимости'
        verbose_name_plural = 'Типы недвижимости'

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', null=True, on_delete=models.CASCADE)
    is_top = models.BooleanField('Рекомендованное', default=False)
    closed = models.BooleanField('Закрыто', default=False)
    is_archive = models.BooleanField('В архиве', default=False)
    # is_important = models.BooleanField('Срочно', default=False)
    # main_photo = FilerImageField(verbose_name='Главное изображение', null=True, blank=True)
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    price = models.DecimalField('Стоимость', null=True, blank=True, decimal_places=0, max_digits=9)
    currency_type = models.ForeignKey(Currency, verbose_name='Валюта', default=1, on_delete=models.SET_DEFAULT)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET(43))
    calendar = ArrayField(DateRangeField(), blank=True, null=True)
    # verified = models.BooleanField('Подтвержден', default=False)

    # reason = models.TextField('Причина', null=True, blank=True)  # налфото(скрытое)

    rooms = models.PositiveSmallIntegerField('Количество комнат', blank=True, null=True)
    floor = models.PositiveSmallIntegerField('Этаж', blank=True, null=True)
    storeys = models.PositiveSmallIntegerField('Этажность здания', null=True, blank=True, )
    landmark = models.CharField('Ориентир', max_length=256, blank=True, null=True)
    total_square = models.FloatField('Общая площадь (метры кв.)', blank=True, null=True)
    living_square = models.FloatField('Жилая площадь (метры кв.)', blank=True, null=True)
    kitchen_square = models.FloatField('Кухонная площадь (метры кв.)', blank=True, null=True)
    district = models.ForeignKey(District, verbose_name='Район', null=True, on_delete=models.CASCADE)
    corner = models.BooleanField('Угловая', default=False, )
    material = models.ForeignKey(Material, verbose_name='Материал', null=True, blank=True, on_delete=models.SET_NULL)
    balcony = models.NullBooleanField('Балкон застеклён', blank=True, null=True)
    loggia = models.NullBooleanField('Лоджия застеклена', blank=True, null=True)
    window = models.ForeignKey(Window, verbose_name='Окно', blank=True, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, verbose_name='Состояние', blank=True, null=True, on_delete=models.SET_NULL)
    # todo: rename  to changed
    created = models.DateTimeField('Дата изменения', auto_now=True, null=True)
    category_tree = models.ForeignKey(TreeCategory, verbose_name='Тип недвижимости', blank=True, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Client, verbose_name='Клиент', blank=True, null=True, on_delete=models.SET_NULL)
    # term = models.DateField

    # hidden

    contacts = models.TextField('Контакты', null=True, blank=True, help_text='Не отображается на сайте')
    private_description = models.TextField('Комментарии от риелтора', null=True, blank=True,
                                           help_text='Не отображается на сайте')
    address = models.TextField('Адрес', null=True, blank=True, help_text='Не отображается на сайте')

    def __str__(self):
        return self.title

    class Meta:
        # index_together = ['verified', 'closed']  # ,'is_top']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class SortableModel(models.Model):
    sort_order = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError('Unknown ordering queryset')

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('sort_order'))
            existing_max = existing_max.get('sort_order__max')
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        qs = self.get_ordering_queryset()
        qs.filter(sort_order__gt=self.sort_order).update(
            sort_order=F('sort_order') - 1)
        super().delete(*args, **kwargs)


class Image(SortableModel):
    image_file = models.ImageField(verbose_name='Изображение',  upload_to='img/%Y/%m/%d', max_length=255)
    product = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        ordering = ('sort_order',)

    def get_ordering_queryset(self):
        return self.product.images.all()


class CustomData(models.Model):
    # USUAL = 0
    # REALTOR = 1
    # USER_TYPES = (
    # 	(USUAL, 'Частное лицо'),
    # 	(REALTOR, 'Риэлтор'),
    # )
    user = models.OneToOneField(User, verbose_name='Пользователь', null=True, related_name='custom',
                                on_delete=models.CASCADE)
    # type = models.IntegerField('Статус', choices=USER_TYPES, default=USUAL)
    phone = models.CharField('Номер телефона', blank=True, max_length=25, null=True)  # 38 050 240 92 92

    # verified = models.BooleanField('Подтвержден', default=False)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Доп информация о пользователе'
        verbose_name_plural = 'Доп информация о пользователе'
