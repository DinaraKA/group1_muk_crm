from django.db import models
from django.contrib.auth.models import User
from accounts.models import StudyGroup


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
        return "%s -  %s мест( %s )" %(self.name, self.places, self.description)


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
    auditoriya = models.ForeignKey(Auditory, related_name='schedule_auditoriya', on_delete=models.CASCADE,
                                   verbose_name='Аудитория')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='schedule_discipline',
                                   verbose_name='Предмет')
    group = models.ForeignKey(StudyGroup, related_name='schedule_group', on_delete=models.CASCADE, verbose_name='Группа')

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s' % (
        self.lesson, self.day, self.teacher, self.auditoriya, self.discipline, self.group)

    class Meta:
        unique_together = ['lesson', 'day', 'group'], ['lesson', 'day', 'teacher'], ['lesson', 'day', 'auditoriya']

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('lesson', 'day', 'group'):
            return 'У выбранной группы есть пара в это время'
        elif model_class == type(self) and unique_check == ('lesson', 'day', 'teacher'):
            return 'У выбранного преподавателя есть пара в это время'
        elif model_class == type(self) and unique_check == ('lesson', 'day', 'auditoriya'):
            return 'Выбранная аудитория занята в это время'
        else:
            return super(Schedule, self).unique_error_message(model_class, unique_check)


    # def avg_grade(self):
    #     grades = Grade.objects.filter(grade=self.pk)
    #     count = 0
    #     for grade in grades:
    #         count += grade.grade
    #     avg = count / len(grades)
    #     avg = round(avg, 1)
    #     return avg


def get_full_name(self):
    return self.last_name + ' ' + self.first_name

User.add_to_class("__str__", get_full_name)


class GroupJournal(models.Model):
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='journal_group', verbose_name='Группа' )
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='journal_discipline', verbose_name='Дисциплина')

    def __str__(self):
        return str(self.study_group) + "-" + str(self.discipline)


class JournalNote(models.Model):
    group_journal = models.ForeignKey(GroupJournal, on_delete=models.CASCADE, related_name='group_journal_note', verbose_name='Журнал группы по дисциплине', default=None )
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    theme = models.CharField(max_length=100, verbose_name='Название занятия/Тема')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='note_created_by', verbose_name='Кем создана')

    def __str__(self):
        return self.theme


class JournalGrade(models.Model):
    journal_note = models.ForeignKey(JournalNote, on_delete=models.PROTECT, related_name='journalnote_grade', verbose_name='Оценка за занятие')
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='note_grade', verbose_name='Оценка')
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_grade', verbose_name='Оценка студенту')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='grade_created_by',
                                   verbose_name='Кем поставлена')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    description = models.CharField(max_length=50, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return  str(self.grade)

    class Meta:
        unique_together = ['journal_note', 'student']