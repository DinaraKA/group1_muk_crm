from django.db import models


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


class Discipline(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False, verbose_name='Дисциплина')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, verbose_name="Пара")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")

    def __str__(self):
        return self.name


