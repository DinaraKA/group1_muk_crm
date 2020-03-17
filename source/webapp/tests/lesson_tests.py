from datetime import datetime

from django.test import TestCase

from webapp.models import Lesson


class LessonModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(
            index=1,
            is_saturday=False,
            start_time='12:12:00',
            end_time='14:14:00'
        )

    def test_object_is_object(self):
        lesson = Lesson.objects.get(id=1)
        self.assertEquals(lesson.index, 1)
        self.assertEquals(lesson.is_saturday, False)
        start_date = datetime(2020, 6, 6, 12, 12, 00)
        self.assertEquals(lesson.start_time.hour, start_date.hour)
        self.assertEquals(lesson.start_time.minute, start_date.minute)
        self.assertEquals(lesson.start_time.second, start_date.second)
        end_date = datetime(2020, 6, 6, 14, 14, 00)
        self.assertEquals(lesson.end_time.hour, end_date.hour)
        self.assertEquals(lesson.end_time.minute, end_date.minute)
        self.assertEquals(lesson.end_time.second, end_date.second)

    def test_verbose_name(self):
        lesson = Lesson.objects.get(id=1)
        field_label = lesson._meta.get_field('index').verbose_name
        self.assertEquals(field_label, 'Порядковый номер')
        field_label = lesson._meta.get_field('is_saturday').verbose_name
        self.assertEquals(field_label, 'Суббота')
        field_label = lesson._meta.get_field('start_time').verbose_name
        self.assertEquals(field_label, 'Время начала')
        field_label = lesson._meta.get_field('end_time').verbose_name
        self.assertEquals(field_label, 'Время окончания')
