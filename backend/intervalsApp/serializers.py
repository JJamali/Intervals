from rest_framework import serializers
from .models import User, IntervalsProfile, RecentResults, Question
import json


# TODO: add validators to fields
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'answers', 'first_note', 'second_note']


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
        user = User(username=validated_data['username'], password=validated_data['password'])
        user.save()

        return user
