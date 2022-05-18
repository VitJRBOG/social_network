from rest_framework import serializers

class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    profile = serializers.IntegerField(source='profile.id')


class BlogPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=140)
    date = serializers.IntegerField()
    blog = serializers.IntegerField(source='blog.id')