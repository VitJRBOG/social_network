from rest_framework import serializers

from .models import Blog, BlogPost

class BlogSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=256)
    profile_id = serializers.IntegerField()

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)


class BlogPostSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=140)
    date = serializers.CharField(max_length=20)
    blog_id = serializers.IntegerField()

    def create(self, validated_data):
        return BlogPost.objects.create(**validated_data)