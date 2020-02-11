from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField


class Role(models.Model):
    name = models.CharField(max_length=500, verbose_name='Роль')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=500, verbose_name='Статус')

    def __str__(self):
        return self.name


class AdminPosition(models.Model):
    name = models.CharField(max_length=500, verbose_name='Должность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class SocialStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name='Социальный статус')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телефона')
    photo = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')
    role = models.ManyToManyField(Role, related_name='role', verbose_name='Роль')
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.CASCADE, related_name='status', verbose_name='Статус',
                               default=None)
    admin_position = models.ForeignKey(AdminPosition, on_delete=models.CASCADE, related_name='admin_position',
                                 verbose_name='Должность', null=True, blank=True)
    social_status = models.ForeignKey(SocialStatus, on_delete=models.CASCADE, related_name='social_status',
                                      verbose_name='Соц. Статус', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


SEX_CHOICES = (
    ('мужской', 'мужской'),
    ("женский", "женский"),
)


class Passport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport', verbose_name='Пользователь')
    citizenship = models.CharField(max_length=20, default="Кыргызская Республика", verbose_name="Гражданство")
    series = models.CharField(max_length=15, verbose_name='Серия')
    issued_by = models.CharField(max_length=255, blank="True", null="True", verbose_name='Кем выдан')
    issued_date = models.DateField(verbose_name='Дата выдачи')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    inn = models.CharField(max_length=50, blank="True", null="True", verbose_name='ИНН')
    nationality = models.CharField(max_length=30, blank="True", null="True", verbose_name='Национальность')
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата Рождения')

    def __str__(self):
        return self.user.get_full_name() + "'s Passport"


class UserAdminPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='position', verbose_name='Пользователь')
    admin_position = models.ForeignKey('AdminPosition', on_delete=models.CASCADE, related_name='position',
                                       verbose_name='Админпоз')

    def __str__(self):
        return self.user.get_full_name()


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Группа')
    students = models.ManyToManyField(User)
    starosta = models.ForeignKey(User, on_delete=models.CASCADE, related_name='starosta', verbose_name='Староста')
    kurator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kurator', verbose_name='Куратор')
    started_at = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return self.name


def get_full_name(self):
    return self.first_name + " " + self.last_name
class Family(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_family', verbose_name='Студент')
    family_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_user', verbose_name='Родственники')

User.add_to_class("__str__", get_full_name)
    def __str__(self):
        return self.family_user.get_full_name()