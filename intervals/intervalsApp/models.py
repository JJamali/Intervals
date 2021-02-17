from django.db import models

# Create your models here.


class User(models.Model):
    level = models.IntegerField(default=0)
    score = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    username = models.CharField(default='', max_length=200)
    # password = models.CharField(default='', max_length=200)

