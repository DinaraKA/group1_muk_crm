from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телеофона')
    photo = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')

    # parent_one = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='parent_one',
    #                                   verbose_name='Родитель Один')
    # parent_two = models.ForeignKey(User, null=True, blank=True,  on_delete=models.PROTECT, related_name='parent_two',
    #                                   verbose_name='Родитель Два')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"


SEX_CHOICES = (
    ('man', 'мужской'),
    ("women", "женский"),
)


class Passport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport', verbose_name='Пользователь')
    series = models.CharField(max_length=15, verbose_name='Серия')
    issued_by = models.CharField(max_length=255, verbose_name='Кем выдан')
    issued_date = models.DateField(verbose_name='Дата выдачи')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    inn = models.CharField(max_length=50, verbose_name='ИНН')
    nationality = models.CharField(max_length=30, verbose_name='Национальность')
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата Рождения')

    def __str__(self):
        return self.user.get_full_name() + "'s Passport"


class AdminPosition(models.Model):
    name = models.CharField(max_length=500, verbose_name='Админпоз')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


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
    name = models.CharField(max_length=500, verbose_name='Социальный статус')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=500, verbose_name='Статус')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Группа')
    students = models.ManyToManyField(User)
    starosta = models.ForeignKey(User, on_delete=models.CASCADE, related_name='starosta', verbose_name='Староста')
    kurator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kurator', verbose_name='Куратор')
    started_at = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return self.name + self.students

class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема')

    def __str__(self):
        return self.name