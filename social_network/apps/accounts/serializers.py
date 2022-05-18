from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    login = serializers.CharField(max_length=25)
    password_hash = serializers.CharField()


class FollowingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    profile = serializers.IntegerField(source='profile.id')
    blog = serializers.IntegerField(source='blog.id')