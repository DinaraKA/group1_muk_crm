from django.test import TestCase
from webapp.models import Schedule, DAY_CHOICES, Discipline, Auditory, Lesson
from accounts.models import Group
from django.contrib.auth.models import User


class ScheduleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(index=1, is_saturday=False, start_time='07:00', end_time='08:00')
        User.objects.create(username='Test')
        Auditory.objects.create(name='555')
        Discipline.objects.create(name='Английский язык')
        Group.objects.create(name="test", starosta_id=1, kurator_id=1, started_at='2020-01-20')
        Schedule.objects.create(lesson_id=1, day=DAY_CHOICES[0], teacher_id=1, auditoriya_id=1, discipline_id=1, group_id=1)

    def test_name_label(self):
        schedule = Schedule.objects.get(id=1)
        field_label = schedule._meta.get_field('lesson').verbose_name
        self.assertEquals(field_label, 'Пара')
        field_label = schedule._meta.get_field('day').verbose_name
        self.assertEquals(field_label, 'День недели')
        field_label = schedule._meta.get_field('teacher').verbose_name
        self.assertEquals(field_label, 'Учитель')
        field_label = schedule._meta.get_field('auditoriya').verbose_name
        self.assertEquals(field_label, 'Аудитория')
        field_label = schedule._meta.get_field('discipline').verbose_name
        self.assertEquals(field_label, 'Предмет')
        field_label = schedule._meta.get_field('group').verbose_name
        self.assertEquals(field_label, 'Группа')