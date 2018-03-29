from rest_framework import serializers

from Main.models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
