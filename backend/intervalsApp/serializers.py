from rest_framework import serializers
from .models import User, IntervalsProfile, RecentResults, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'answers', 'first_note', 'second_note', 'answered']


class RecentResultsSerializer(serializers.ModelSerializer):
    """Serializes recent results for the level that the user is currently on."""
    class Meta:
        model = RecentResults
        fields = ['level', 'total_correct', 'total_completed', 'recent_results']


class StatsSerializer(serializers.ModelSerializer):
    recent = RecentResultsSerializer(many=True, read_only=True)

    class Meta:
        model = IntervalsProfile
        fields = ['level', 'recent']


class SettingsSerializer(serializers.ModelSerializer):
    """Serializes settings that pertain to user, such as level, note order, and speed."""
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


class BaseUserSerializer(serializers.ModelSerializer):
    """Provides behaviours that apply to all UserSerializers."""
    def to_representation(self, instance):
        """Show 'Guest' as username if user is a guest."""
        ret = super().to_representation(instance)
        if instance.is_guest:
            ret['username'] = 'Guest'
        return ret


class UserSerializer(BaseUserSerializer):
    stats = StatsSerializer(source='profile', required=True)
    settings = SettingsSerializer(source='profile', required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'stats', 'settings']
        extra_kwargs = {"password": {'write_only': True}}


class BriefUserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(source='pk', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_guest']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_guest': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class ConvertGuestToUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {"password": {'write_only': True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.set_password(validated_data.get('password'))
        instance.is_guest = False
        instance.save()

        return instance
