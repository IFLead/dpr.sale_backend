from django.contrib.auth.models import User
from rest_framework import serializers

from Main.models import Post, Category, Currency, TreeCategory, State, Window, Material, City, District, CustomData, \
	Image


class MyImageSerializer(serializers.ModelSerializer):
	url = serializers.CharField(source='image_file.url')

	class Meta:
		model = Image
		fields = ('id', 'url')
		related_fields = ['image_file']


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = (
		'id', 'is_top', 'title', 'price', 'created', 'category', 'main_photo', 'currency_type', 'category_tree',
		'district')


class SinglePostSerializer(serializers.ModelSerializer):
	images = MyImageSerializer(many=True)
	related_fields = ['main_photo']
	main_photo_url = serializers.CharField(source='main_photo.url', allow_blank=True, required=False, )

	class Meta:
		model = Post
		fields = ('id', 'is_top', 'title', 'description', 'price', 'closed', 'rooms', 'floor', 'storeys', 'landmark',
		'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony', 'loggia', 'created',
		'category_tree', 'main_photo_url', 'currency_type', 'owner', 'district', 'material',
		'window', 'state', 'images')


class PostUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'


class DefaultUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = Currency
		fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
	class Meta:
		model = State
		fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Material
		fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Window
		fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = City
		fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
	class Meta:
		model = District
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomData
		fields = ('id', 'first_name', 'last_name', 'phone')
		related_fields = ['user']

	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	id = serializers.IntegerField(source='user.id')


class TreeCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TreeCategory
		fields = '__all__'
