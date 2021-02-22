from rest_framework import serializers
from .models import User
from .models import IntervalsProfile
from rest_framework_simplejwt.settings import api_settings


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


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
