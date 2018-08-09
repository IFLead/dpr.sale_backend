from django.contrib.auth.models import User
from rest_framework import serializers

from Main.models import Post, Category, Currency, TreeCategory, State, Window, Material, City, District, CustomData, \
    Image, Client


class MyImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='image_file.url')

    class Meta:
        model = Image
        fields = ('id', 'url')
        related_fields = ['image_file']


class PostSerializer(serializers.ModelSerializer):
    images = MyImageSerializer(many=True)

    class Meta:
        model = Post
        fields = (
        'id', 'is_top', 'title', 'price', 'created', 'category', 'images', 'currency_type', 'category_tree',
        'district')


class AllPostSerializer(serializers.ModelSerializer):

    images = MyImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class SinglePostSerializer(serializers.ModelSerializer):
    images = MyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'is_top', 'title', 'description', 'price', 'closed', 'rooms', 'floor', 'storeys', 'landmark',
                  'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony', 'loggia', 'created',
                  'category_tree', 'currency_type', 'owner', 'district', 'material',
                  'window', 'state', 'images')


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'is_top', 'title', 'description', 'price', 'closed', 'rooms', 'floor', 'storeys', 'landmark',
        'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony', 'loggia', 'created',
        'category_tree', 'currency_type', 'owner', 'district', 'material',
        'window', 'state', 'is_archive', 'closed')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('is_top', 'title', 'description', 'price', 'closed', 'rooms', 'floor', 'storeys', 'landmark',
        'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony', 'loggia',
        'category_tree', 'currency_type', 'district', 'material',
        'window', 'state', 'is_archive', 'closed')


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


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name', 'decription', 'phone_one', 'phone_two', 'phone_three', 'phone_four')


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
        fields = ('id', 'first_name', 'last_name', 'phone', 'username')
        related_fields = ['user']

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    id = serializers.IntegerField(source='user.id')


class TreeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeCategory
        fields = '__all__'
