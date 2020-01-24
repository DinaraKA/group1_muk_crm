from django.contrib.auth.models import User
from django.db import models
from phone_field import PhoneField

from webapp.models import Discipline, Grade


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
    name = models.CharField(max_length=500, verbose_name='Социальный статус')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    phone_number = PhoneField(null=True, blank=True, verbose_name='Номер телеофона')
    photo = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Фото')
    address_fact = models.CharField(max_length=100, verbose_name='Фактический Адрес')
    role = models.ManyToManyField(Role, related_name='role', verbose_name='Роль')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status', verbose_name='Статус',
                               default=None)
    admin_position = models.ForeignKey(AdminPosition, on_delete=models.CASCADE, related_name='admin_position',
                                 verbose_name='Должность', null=True, blank=True)
    social_status = models.ForeignKey(SocialStatus, on_delete=models.CASCADE, related_name='social_status',
                                      verbose_name='Соц. Статус', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"


SEX_CHOICES = (
    ('man', 'мужской'),
    ("women", "женский"),
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
    citizenship = models.CharField(max_length=20, default='Кыргызстан')

    def __str__(self):
        return self.user.get_full_name() + "'s Passport"


class UserAdminPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='position', verbose_name='Пользователь')
    admin_position = models.ForeignKey('AdminPosition', on_delete=models.CASCADE, related_name='position',
                                       verbose_name='Админпоз')

    def __str__(self):
        return self.user.get_full_name()


# class UserRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role', verbose_name='Пользователь')
#     role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role', verbose_name='Роль')
#
#     def __str__(self):
#         return self.user.get_full_name()



class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Группа')
    students = models.ManyToManyField(User)
    starosta = models.ForeignKey(User, on_delete=models.CASCADE, related_name='starosta', verbose_name='Староста')
    kurator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kurator', verbose_name='Куратор')
    started_at = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема')

    def __str__(self):
        return self.name

class Progress(models.Model):
    date = models.DateField(verbose_name='Дата')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student', verbose_name='Студент')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='dicipline', verbose_name='Дисциплина')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme', verbose_name='Тема')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade', verbose_name='Оценка')

    def __str__(self):
        return self.student.last_name + self.student.first_name
