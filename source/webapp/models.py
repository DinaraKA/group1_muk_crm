# from django.db import models
# from django.contrib.auth.models import User
#
# STATUS = (
#     ('student', 'Другое'),
#     ('personal', 'Персонал'),
# )
#
#
# class Passport(models.Model):
#     document = models.IntegerField(max_length=20, verbose_name='Серия')
#     authority = models.CharField(max_length=50, verbose_name='Кем выдан')
#     place_of_birth = models.CharField(max_length=50, verbose_name='Место рождения')
#     date_of_issue = models.DateField(null=True, blank=True, verbose_name='Дата выдачи')
#     personal_number = models.IntegerField(max_length=20, verbose_name='ИНН')
#     sex = models.CharField(max_length=50, verbose_name='Пол')
#     birth_date = models.DateField(verbose_name='Дата рождения')
#     citizenship = models.CharField(max_length=50, verbose_name='Гражданство')
#     natiaonality = models.CharField(max_length=50, verbose_name='Национальность')
#     user = models.OneToOneField(User, related_name='passport', on_delete=models.CASCADE, verbose_name='Пользователь')
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
#     status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0][0],
#                                 verbose_name='Категория')
#     avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
#     position = models.CharField(null=True, blank=True,max_length=50, verbose_name='Должность')
#     phone = models.IntegerField(max_length=20, verbose_name='Телефон')
#     adress = models.CharField(max_length=50, verbose_name='Адрес')
#     passport = models.ForeignKey(Passport, on_delete=models.CASCADE, verbose_name='Пасспорт')
#
#
#     def __str__(self):
#         return self.user.get_full_name() + "'s Profile"
#
#     class Meta:
#         verbose_name = 'Профиль'
#         verbose_name_plural = 'Профили'

# Create your models here.
