from rest_framework import serializers

from Main.models import Post, Category, Currency, TreeCategory, State, Window, Material, City, District, User, CustomData


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'price', 'created', 'category', 'main_photo', 'currency_type')


class SinglePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'is_top', 'title', 'description', 'price', 'closed', 'rooms', 'floor', 'storeys', 'landmark',
		'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony', 'loggia', 'created',
		'category', 'main_photo', 'currency_type', 'owner', 'district', 'material',
		'window', 'state')


class PostUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
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
		fields = ('user_id', 'first_name', 'last_name', 'phone')
		related_fields = ['user']

	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	user_id = serializers.IntegerField(source='user.id')


class TreeCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TreeCategory
		fields = '__all__'


