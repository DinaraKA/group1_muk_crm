from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.ForeignKey(User, related_name='parents', on_delete=models.CASCADE, verbose_name='Родитель')

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телеофона')
    photo = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')
    parent_one = models.OneToOneField(User, related_name='profile', verbose_name='Родитель Один')
    parent_two = models.OneToOneField(User, related_name='profile', verbose_name='Родитель Два')

class Passport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passport', verbose_name='Паспорт')
    series = models.IntegerField(max_length=30, verbose_name='Серия')
    issued_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    issued_date = models.DateField(verbose_name='Дата выдачи')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    inn = models.IntegerField(max_length=50, verbose_name='ИНН')
    nationality = models.CharField(max_length=30, verbose_name='Национальность')
    sex = models.CharField(max_length=15, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата Рождения')