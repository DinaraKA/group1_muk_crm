from django.contrib.auth.models import User
from django.db import models

class Parent(models.Model):
    user = models.ForeignKey(User, related_name='parents', on_delete=models.CASCADE, verbose_name='Родитель')

    def __str__(self):
        return str(self.id)