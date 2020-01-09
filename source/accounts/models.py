from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Passport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport', verbose_name='Пользователь', default=None)
    series = models.CharField(max_length=15, verbose_name='Серия')
    issued_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    issued_date = models.DateField(verbose_name='Дата выдачи')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    inn = models.CharField(max_length=50, verbose_name='ИНН')
    nationality = models.CharField(max_length=30, verbose_name='Национальность')
    sex = models.CharField(max_length=15, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата Рождения')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"


class ParentOne(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_one', verbose_name='Родитель 1')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"


class ParentTwo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_two', verbose_name='Родитель 2')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телеофона')
    photo = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')
    parent_one = models.ForeignKey(ParentOne, on_delete=models.PROTECT, related_name='parent_one',
                                      verbose_name='Родитель Один', null=True, blank=True)
    parent_two = models.ForeignKey(ParentTwo, on_delete=models.PROTECT, related_name='parent_two',
                                      verbose_name='Родитель Два', null=True, blank=True)
    # passport = models.OneToOneField(Passport, related_name='passport', verbose_name='Паспорт', on_delete=models.CASCADE,
    #                                 default=None, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"



class AdminPosition(models.Model):
    name = models.CharField(max_length=500, verbose_name='Админпоз')

    def __str__(self):
        return self.name


class UserAdminPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='position', verbose_name='Пользователь')
    admin_position = models.ForeignKey('AdminPosition', on_delete=models.CASCADE, related_name='position',
                                       verbose_name='Админпоз')

    def __str__(self):
        return self.user.get_full_name()


class Role(models.Model):
    name = models.CharField(max_length=500, verbose_name='Роль')

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role', verbose_name='Пользователь')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role', verbose_name='Роль')

    def __str__(self):
        return self.user.get_full_name()


class SocialStatus(models.Model):
    name = models.CharField(max_length=500, verbose_name='Статус')

    def __str__(self):
        return self.name


class UserSocialStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='socstatus', verbose_name='Пользователь')
    status = models.ForeignKey('SocialStatus', on_delete=models.CASCADE, related_name='socstatus', verbose_name='Cтатус')

    def __str__(self):
        return self.user.get_full_name()