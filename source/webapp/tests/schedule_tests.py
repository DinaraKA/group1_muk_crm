from django.test import TestCase
from webapp.models import Schedule, DAY_CHOICES, Discipline, Auditory, Lesson
from accounts.models import StudyGroup
from django.contrib.auth.models import User


class ScheduleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(index=1, is_saturday=False, start_time='12:00', end_time='12:20')
        User.objects.create(username='Test')
        Auditory.objects.create(name='555')
        Discipline.objects.create(name='Английский язык')
        StudyGroup.objects.create(name="test", group_leader_id=1, head_teaher_id=1, started_at='2020-01-20')
        Schedule.objects.create(lesson_id=1, day=DAY_CHOICES[0], teacher_id=1, auditoriya_id=1, discipline_id=1,
                                group_id=1)

    def test_object_is_object(self):
        schedule = Schedule.objects.get(id=1)
        self.assertEquals(schedule.lesson.index, 1)
        self.assertEquals(schedule.lesson.index, 1)
        self.assertEquals(schedule.day, 'Понедельник')
        self.assertEquals(schedule.teacher.username, 'Test')
        self.assertEquals(schedule.auditoriya.name, '555')
        self.assertEquals(schedule.discipline.name, 'Английский язык')
        self.assertEquals(schedule.group.name, 'test')

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