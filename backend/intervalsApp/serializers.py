from rest_framework import serializers
from .models import User, IntervalsProfile, RecentResults


class RecentResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentResults
        fields = ['level', 'total_correct', 'total_completed', 'recent_results']


class ProfileSerializer(serializers.ModelSerializer):
    recent = RecentResultsSerializer(many=True, read_only=True)

    class Meta:
        model = IntervalsProfile
        fields = ['level', 'current_level', 'recent', 'note_order', 'playback_speed']

    def update(self, instance, validated_data):
        instance.current_level = validated_data.get('current_level', instance.current_level)
        instance.note_order = validated_data.get('note_order', instance.note_order)
        instance.playback_speed = validated_data.get('playback_speed', instance.playback_speed)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        # Create user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
