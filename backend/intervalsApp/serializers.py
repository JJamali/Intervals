from rest_framework import serializers
from .models import User
from .models import IntervalsProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalsProfile
        fields = ['user', 'level', 'total_correct', 'total_completed', 'recent_results']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        # Create user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # Create profile
        IntervalsProfile.objects.create(user=user, level=0, total_correct=0, total_completed=0, recent_results=[])

        return user


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

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


# Allows for extraction of other important information along with token e.g. user information
# Encodes non-username/password information in the access token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # Customize the JWT response (the response, not the token) to include user information
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
