from django.contrib.auth.models import User
from django.db import models

<<<<<<< HEAD
class Parent(models.Model):
    user = models.ForeignKey(User, related_name='parents', on_delete=models.CASCADE, verbose_name='Родитель')

    def __str__(self):
        return str(self.id)
=======

class News(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    photo = models.ImageField(upload_to='news_images', null=False, blank=False, verbose_name='Фото')

    def __str__(self):
        return self.title


>>>>>>> bc1c1fef9ef688f469f7466a02245bcd8e21025d
