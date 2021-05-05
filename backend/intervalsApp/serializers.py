from rest_framework import serializers
from .models import User, IntervalsProfile, RecentResults, Question
import json


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'answers', 'first_note', 'second_note', 'answered']


class RecentResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentResults
        fields = ['level', 'total_correct', 'total_completed', 'recent_results']


class StatsSerializer(serializers.ModelSerializer):
    recent = RecentResultsSerializer(many=True, read_only=True)

    class Meta:
        model = IntervalsProfile
        fields = ['level', 'recent']


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalsProfile
        fields = ['current_level', 'note_order', 'playback_speed']
        extra_kwargs = {
            'current_level': {'required': True},
            'note_order': {'required': True},
            'playback_speed': {'required': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate_current_level(self, value):
        if value < 0:
            raise serializers.ValidationError("Current level cannot be negative")
        if value > self.instance.level:
            raise serializers.ValidationError("Current level cannot be higher than level")
        return value


class UserSerializer(serializers.ModelSerializer):
    stats = StatsSerializer(source='profile', required=True)
    settings = SettingsSerializer(source='profile', required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'stats', 'settings']
        extra_kwargs = {"password": {'write_only': True}}


class BriefUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        read_only_fields = ['id']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        user = User(username=validated_data['username'])
        user.set_password(password)
        user.save()

        return user
