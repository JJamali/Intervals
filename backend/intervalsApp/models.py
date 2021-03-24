from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    pass


class IntervalsProfile(models.Model):
    # Belongs to User model in 1-to-1 relationship.
    # If User is deleted, then the corresponding IntervalsProfile will be deleted as well.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)  # Total correct answers within that level
    total_completed = models.IntegerField(default=0)  # Total answers within that level
    recent_results = ArrayField(models.BooleanField(), size=apps.get_app_config('intervalsApp').SCORE_RANGE, default=list)  # Uses postgres ArrayField


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created(sender, instance, created, **kwargs):
    if created:
        IntervalsProfile.objects.create(user=instance)
