from rest_framework import serializers

from Main.models import Post, Category, Currency


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'price', 'created', 'category', 'main_photo', 'currency')


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
