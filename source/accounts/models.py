from django.contrib.auth.models import User
from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

class Parent(models.Model):
    user = models.ForeignKey(User, related_name='parents', on_delete=models.CASCADE, verbose_name='Родитель')

    def __str__(self):
        return str(self.id)
