from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Group


class News(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    photo = models.ImageField(upload_to='news_images', null=False, blank=False, verbose_name='Фото')

    def __str__(self):
        return self.title


class Announcements(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    photo = models.ImageField(upload_to='announce_image', null=False, blank=False, verbose_name='Фото')

    def __str__(self):
        return self.title


class Auditory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название')
    places = models.IntegerField(null=True, blank=True, verbose_name='Вместимость')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class Grade(models.Model):
    value = models.CharField(max_length=50, null=True, blank=True, verbose_name='Оценка')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Discipline(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False, verbose_name='Дисциплина')
    teacher = models.ManyToManyField(User, related_name='disciplines', verbose_name='Преподаватель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class Lesson(models.Model):
    index = models.IntegerField(verbose_name="Порядковый номер")
    is_saturday = models.BooleanField(verbose_name="Суббота")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")

    def __str__(self):
        return str(self.index) + " пара"

DAY_CHOICES = (
    ('Monday', 'Понедельник'),
    ('Tuesday', "Вторник"),
    ('Wednesday', 'Среда'),
    ('Thursday', "Четверг"),
    ('Friday', "Пятница"),
    ('Saturday', "Суббота")
)
class Schedule(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='schedule_lesson', on_delete=models.CASCADE, verbose_name='Пара')
    day = models.CharField(max_length=20, choices=DAY_CHOICES, verbose_name='День недели')
    teacher = models.ForeignKey(User, related_name='schedule_user', on_delete=models.CASCADE, verbose_name='Учитель')
    auditoriya = models.ForeignKey(Auditory, related_name='schedule_auditoriya', on_delete=models.CASCADE, verbose_name='Аудитория')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='schedule_discipline', verbose_name='Предмет')
    group = models.ForeignKey(Group, related_name='schedule_group', on_delete=models.CASCADE, verbose_name='Группа')

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s' % (self.lesson, self.day, self.teacher, self.auditoriya, self.discipline, self.group)

    # def __str__(self):
    #     return self.objects

class Theme(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='theme_discipline', verbose_name='Дисциплина')

    def __str__(self):
        return self.name


class Journal(models.Model):
    date = models.DateField(verbose_name='Дата')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student', verbose_name='Студент')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='discipline', verbose_name='Дисциплина')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme', verbose_name='Тема')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade', verbose_name='Оценка')

    def __str__(self):
        return self.student.last_name + self.student.first_name
