from django.test import TestCase
from webapp.models import Schedule


class ScheduleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Schedule.objects.create(event='TestModel')

    def test_name_label(self):
        schedule = Schedule.objects.get(id=1)
        field_label = schedule._meta.get_field('event').verbose_name
        self.assertEquals(field_label, 'Событие')
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