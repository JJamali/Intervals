from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class User(models.Model):
    level = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2)