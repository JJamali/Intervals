from rest_framework import serializers
from .models import User
from .models import IntervalsProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalsProfile
        fields = ['level', 'score']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        # Create user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # Create profile
        IntervalsProfile.objects.create(user=user, **profile_data)

        return user
