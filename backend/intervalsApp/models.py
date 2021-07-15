from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    is_guest = models.BooleanField(default=False)


class IntervalsProfile(models.Model):
    """
    Belongs to User model in 1-to-1 relationship.
    If User is deleted, then the corresponding IntervalsProfile will be deleted as well.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    current_level = models.IntegerField(default=0)  # Level the user is currently viewing/on

    class PlaybackSpeed(models.TextChoices):
        """Uses Django enumeration type to nicely define playback speed choices.

        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types"""
        SLOW = 'S'
        NORMAL = 'N'
        FAST = 'F'

    playback_speed = models.CharField(
        max_length=1,
        choices=PlaybackSpeed.choices,
        default=PlaybackSpeed.NORMAL
    )

    class NoteOrder(models.TextChoices):
        """Uses Django enumeration type to nicely define note order choices.

        https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types"""
        IN_ORDER = 'O'
        BACKWARDS = 'B'
        RANDOM = 'R'

    note_order = models.CharField(
        max_length=1,
        choices=NoteOrder.choices,
        default=NoteOrder.IN_ORDER
    )

    def recent_results_at_level(self, level=None):
        # If no level is passed, the user's current level will be used
        if level is None:
            level = self.level
        # Returns RecentResults object that has the current profile and given level
        recent_results, created = RecentResults.objects.get_or_create(profile=self, level=level)
        return recent_results

    def all_recent_results(self):
        """Returns a dictionary of this profile's RecentResults objects.

        Dictionary maps RecentResults level to RecentResults object."""

        results_queryset = RecentResults.objects.filter(profile=self)

        results_dict = {}
        for r in results_queryset:
            results_dict[r.level] = r

        return results_dict


class Question(models.Model):
    """
    Has a 1-to-1 relationship with IntervalsProfile.
    Represents current question the user is viewing.
    """
    profile = models.OneToOneField(IntervalsProfile, related_name='question', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)  # Actual question text e.g. "This is a question"
    answers = ArrayField(models.CharField(max_length=1000))  # Array of answers
    correct_answer = models.CharField(max_length=1000)
    first_note = models.IntegerField(default=0)
    second_note = models.IntegerField(default=0)

    answered = models.BooleanField(default=False)


class RecentResults(models.Model):
    """
    Each IntervalsProfile has a RecentResult for each level.
    Therefore, RecentResults is mapped to IntervalsProfile in a many-to-1 relationship.
    If IntervalsProfile is deleted, then all corresponding RecentResults will be deleted as well.
    """
    profile = models.ForeignKey(IntervalsProfile, on_delete=models.CASCADE, related_name='recent')
    recent_results = ArrayField(models.BooleanField(), size=apps.get_app_config('intervalsApp').SCORE_RANGE, default=list)  # Uses postgres ArrayField
    level = models.IntegerField()
    total_correct = models.IntegerField(default=0)  # Total correct answers within that level
    total_completed = models.IntegerField(default=0)  # Total answers within that level


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created(sender, instance, created, **kwargs):
    if created:
        IntervalsProfile.objects.create(user=instance)


# Create RecentResults for the starting level
@receiver(post_save, sender=IntervalsProfile)
def profile_created(sender, instance, created, **kwargs):
    if created:
        RecentResults.objects.create(profile=instance, level=instance.level)
