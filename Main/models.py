from django.contrib.auth.models import User
from django.db import models
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
	name = models.CharField('Название', max_length=128)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Currency(models.Model):
	name = models.CharField('Название', max_length=128)
	symbol = models.CharField('Символ', max_length=2)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Валюта'
		verbose_name_plural = 'Валюты'


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


class Living_space(models.Model):
	name = models.CharField('Тип', max_length=55)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Жилая площадь'
		verbose_name_plural = 'Жилые площади'


class TreeCategory(MPTTModel):
	name = models.CharField(max_length=50)
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

	def __str__(self):
		# if self.is_leaf_node():
		return self.get_level() * '-' + self.name

	class Meta:
		verbose_name = 'Дерево категорий'
		verbose_name_plural = 'Деревья категорий'

	class MPTTMeta:
		order_insertion_by = ['name']


class Post(models.Model):
	category = models.ForeignKey(Category, verbose_name='Категория')
	is_top = models.BooleanField('Рекомендованное', default=False)
	# is_important = models.BooleanField('Срочно', default=False)
	main_photo = FilerImageField(verbose_name='Главное изображение', null=True, blank=True)
	title = models.CharField('Заголовок', max_length=256)
	description = models.TextField('Описание')
	price = models.DecimalField('Стоимость', null=True, blank=True, decimal_places=0, max_digits=9)
	currency_type = models.ForeignKey(Currency, verbose_name='Валюта', default=1)
	owner = models.ForeignKey(User, verbose_name='Владелец')
	# verified = models.BooleanField('Подтвержден', default=False)
	closed = models.BooleanField('Закрыт', default=False)
	# reason = models.TextField('Причина', null=True, blank=True)  # налфото(скрытое)

	rooms = models.PositiveSmallIntegerField('Количество комнат', blank=True, null=True)
	floor = models.PositiveSmallIntegerField('Этаж', blank=True, null=True)
	storeys = models.PositiveSmallIntegerField('Этажность здания', default=1, null=True)
	landmark = models.CharField('Ориентир', max_length=256, blank=True, null=True)
	total_square = models.FloatField('Общая площадь (метры кв.)', blank=True, null=True)
	living_square = models.FloatField('Жилая площадь (метры кв.)', blank=True, null=True)
	kitchen_square = models.FloatField('Кухонная площадь (метры кв.)', blank=True, null=True)
	district = models.ForeignKey(District, verbose_name='Район', null=True, )
	corner = models.BooleanField('Угловая', default=False, )
	material = models.ForeignKey(Material, verbose_name='Материал', null=True, )
	balcony = models.NullBooleanField('Балкон застеклён', blank=True, null=True)
	loggia = models.NullBooleanField('Лоджия застеклена', blank=True, null=True)
	window = models.ForeignKey(Window, verbose_name='Окно', blank=True, null=True)
	state = models.ForeignKey(State, verbose_name='Состояние', blank=True, null=True)
	created = models.DateTimeField('Дата создания', auto_now=True, null=True)
	category_tree = models.ForeignKey(TreeCategory, verbose_name='Дерево состояний', blank=True, null=True)
	# term = models.DateField

	# hidden

	contacts = models.TextField('Контакты', null=True, blank=True)
	private_description = models.TextField('Комментарии от риелтора', null=True, blank=True)
	address = models.TextField('Адрес', null=True, blank=True)

	def __str__(self):
		return self.title

	class Meta:
		# index_together = ['verified', 'closed']  # ,'is_top']
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'


class Image(models.Model):
	image_file = FilerImageField(verbose_name='Изображение', )
	obj = models.ForeignKey(Post, related_name='photos')


class CustomData(models.Model):
	# USUAL = 0
	# REALTOR = 1
	# USER_TYPES = (
	# 	(USUAL, 'Частное лицо'),
	# 	(REALTOR, 'Риэлтор'),
	# )
	user = models.OneToOneField(User, verbose_name='Пользователь', null=True, related_name='custom')
	# type = models.IntegerField('Статус', choices=USER_TYPES, default=USUAL)
	phone = models.CharField('Номер телефона', blank=True, max_length=25, null=True)  # 38 050 240 92 92

	# verified = models.BooleanField('Подтвержден', default=False)

	def __str__(self):
		return self.user.first_name

	class Meta:
		verbose_name = 'Доп информация о пользователе'
		verbose_name_plural = 'Доп информация о пользователе'
