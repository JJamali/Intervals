from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User section


class User(AbstractUser):
    pass


class IntervalsProfile(models.Model):
    # Belongs to User model in 1-to-1 relationship.
    # If User is deleted, then the corresponding IntervalsProfile will be deleted as well.
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2)


# Quiz section


# class Question(models.Model):
#     question = models.CharField(...)
#
#     def check_answer(self, choice):
#         return self.choice_set.filter(id=choice.id, is_answer=True).exists()
#
#     def get_answers(self):
#         return self.choice_set.filter(is_answer=True)

#
# class Choice(models.Model):
#     question = models.ForeignKey('Question')
#     choice = models.CharField(...)
#     is_answer = models.BooleanField(default=False)
#
#
# class Answer(models.Model):
#     question = models.ForeignKey("Question")
#     answers = models.ForeignKey("Choice")
