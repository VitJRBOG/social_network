from rest_framework import serializers

from .models import Profile, Following

class ProfileSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=256)
    login = serializers.CharField(max_length=25)
    password_hash = serializers.CharField()

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)


class FollowingSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    profile_id = serializers.IntegerField()
    blog_id = serializers.IntegerField()

    def create(self, validated_data):
        return Following.objects.create(**validated_data)