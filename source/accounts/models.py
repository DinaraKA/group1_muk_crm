from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телеофона')
    photo = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')
    parent_one = models.OneToOneField(User, related_name='profile', verbose_name='Родитель Один')
    parent_two = models.OneToOneField(User, related_name='profile', verbose_name='Родитель Два')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"
