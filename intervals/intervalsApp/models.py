from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class IntervalsProfile(models.Model):
    # Belongs to User model in 1-to-1 relationship.
    # If User is deleted, then the corresponding IntervalsProfile will be deleted as well.
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2)
