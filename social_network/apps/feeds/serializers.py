from rest_framework import serializers


class FeedPostSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.IntegerField(source='profile.id')
    blogpost = serializers.IntegerField(source='blogpost.id')
    is_read = serializers.BooleanField()