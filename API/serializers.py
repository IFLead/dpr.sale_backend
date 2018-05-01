from rest_framework import serializers

from Main.models import Post, Category, Currency, TreeCategory


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'title', 'price', 'created', 'category', 'main_photo', 'currency_type')


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


class TreeCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = TreeCategory
		fields = '__all__'
