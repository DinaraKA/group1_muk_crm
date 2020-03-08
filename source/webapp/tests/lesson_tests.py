from datetime import datetime

from selenium.webdriver import Chrome

from django.test import TestCase
from django.urls import reverse, reverse_lazy, resolve

from webapp.models import Lesson
from webapp.views import LessonListView, LessonCreateView


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


class LessonViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_lesson(self):
        self.driver.get('http://localhost:8000/lessons/all/')
        assert self.driver.current_url == 'http://localhost:8000/lessons/all/'

    def test_created_lesson(self):
        self.driver.get('http://localhost:8000/lessons/add/')
        self.driver.find_element_by_name('index').send_keys(1)
        self.driver.find_element_by_name('is_saturday').send_keys(False)
        self.driver.find_element_by_name('start_time').send_keys('12:12:00')
        self.driver.find_element_by_name('end_time').send_keys('14:14:00')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/lessons/all/'

    def test_updated_lesson(self):
        self.driver.get('http://127.0.0.1:8000/lessons/update/1/')
        self.driver.find_element_by_name('index').clear()
        self.driver.find_element_by_name('is_saturday').click()
        self.driver.find_element_by_name('start_time').clear()
        self.driver.find_element_by_name('end_time').clear()
        self.driver.find_element_by_name('index').send_keys(2)
        self.driver.find_element_by_name('is_saturday').send_keys(True)
        self.driver.find_element_by_name('start_time').send_keys('13:13:00')
        self.driver.find_element_by_name('end_time').send_keys('15:15:00')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/lessons/all/'

    def test_deleted_lesson(self):
        self.driver.get('http://127.0.0.1:8000/lessons/delete/1')
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/lessons/all/'


class LessonUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(
            index=1,
            is_saturday=False,
            start_time='12:12:00',
            end_time='14:14:00'
        )

    def test_list_url_is_resolved(self):
        url = reverse('webapp:lessons')
        self.assertEquals(resolve(url).func.view_class, LessonListView)

    def test_create_url_is_resolved(self):
        url = reverse('webapp:lesson_create')
        self.assertEquals(resolve(url).func.view_class, LessonCreateView)
