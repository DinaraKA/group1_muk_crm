from datetime import datetime

from selenium.webdriver import Chrome

from django.test import TestCase
from django.urls import reverse, reverse_lazy, resolve

from webapp.models import Lesson
from webapp.views import LessonListView, LessonCreateView


class AuditoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(
            index=1,
            is_saturday=False,
            start_time='12:12:00',
            end_time='14:14:00'
        )

    def test_index_field(self):
        auditory = Lesson.objects.get(id=1)
        self.assertEquals(auditory.index, 1)

    def test_is_saturday_field(self):
        lesson = Lesson.objects.get(id=1)
        self.assertEquals(lesson.is_saturday, False)

    def test_start_time_field(self):
        lesson = Lesson.objects.get(id=1)
        date = datetime(2020, 6, 6, 12, 12, 00)
        self.assertEquals(lesson.start_time.hour, date.hour)
        self.assertEquals(lesson.start_time.minute, date.minute)
        self.assertEquals(lesson.start_time.second, date.second)

    def test_end_time_field(self):
        lesson = Lesson.objects.get(id=1)
        date = datetime(2020, 6, 6, 14, 14, 00)
        self.assertEquals(lesson.end_time.hour, date.hour)
        self.assertEquals(lesson.end_time.minute, date.minute)
        self.assertEquals(lesson.end_time.second, date.second)

    def test_index_verbose_name(self):
        passport = Lesson.objects.get(id=1)
        field_label = passport._meta.get_field('index').verbose_name
        self.assertEquals(field_label, 'Порядковый номер')

    def test_is_saturday_verbose_name(self):
        passport = Lesson.objects.get(id=1)
        field_label = passport._meta.get_field('is_saturday').verbose_name
        self.assertEquals(field_label, 'Суббота')

    def test_start_time_verbose_name(self):
        passport = Lesson.objects.get(id=1)
        field_label = passport._meta.get_field('start_time').verbose_name
        self.assertEquals(field_label, 'Время начала')

    def test_end_time_verbose_name(self):
        passport = Lesson.objects.get(id=1)
        field_label = passport._meta.get_field('end_time').verbose_name
        self.assertEquals(field_label, 'Время окончания')


class AuditoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Lesson.objects.create(
            index=1,
            is_saturday=False,
            start_time='12:12:00',
            end_time='14:14:00'
        )

    def test_lesson_list(self):
        response = self.client.get(reverse('webapp:lessons'))
        start_time = datetime(2020, 6, 6, 12, 12, 00)
        end_time = datetime(2020, 6, 6, 14, 14, 00)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 1)
        self.assertContains(response, start_time.hour)
        self.assertContains(response, start_time.minute)
        self.assertContains(response, start_time.second)
        self.assertContains(response, end_time.hour)
        self.assertContains(response, end_time.minute)
        self.assertContains(response, end_time.second)

    def test_created_lesson(self):
        response = self.client.post(reverse('webapp:lesson_create'), {
            'index': 1,
            'is_saturday': False,
            'start_time': '12:12:00',
            'end_time': '14:14:00',
        })
        start_time = datetime(2020, 6, 6, 12, 12, 00)
        end_time = datetime(2020, 6, 6, 14, 14, 00)
        self.assertEqual(Lesson.objects.get(pk=1).index, 1)
        self.assertEqual(Lesson.objects.get(pk=1).is_saturday, False)
        self.assertEqual(Lesson.objects.get(pk=1).start_time.hour, start_time.hour)
        self.assertEqual(Lesson.objects.get(pk=1).start_time.minute, start_time.minute)
        self.assertEqual(Lesson.objects.get(pk=1).start_time.second, start_time.second)
        self.assertEqual(Lesson.objects.get(pk=1).end_time.hour, end_time.hour)
        self.assertEqual(Lesson.objects.get(pk=1).end_time.minute, end_time.minute)
        self.assertEqual(Lesson.objects.get(pk=1).end_time.second, end_time.second)
        self.assertEqual(response.status_code, 302)

    def test_updated_lesson(self):
        lesson = Lesson.objects.get(id=1)
        response = self.client.post(
            reverse('webapp:lesson_update', kwargs={'pk': lesson.pk}),
            {
                'index': 2,
                'is_saturday': True,
                'start_time': '13:13:00',
                'end_time': '15:15:00',
            })
        start_time = datetime(2020, 6, 6, 13, 13, 00)
        end_time = datetime(2020, 6, 6, 15, 15, 00)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lesson.objects.get().index, 2)
        self.assertEqual(Lesson.objects.get().is_saturday, True)
        self.assertEqual(Lesson.objects.get().start_time.hour, start_time.hour)
        self.assertEqual(Lesson.objects.get().start_time.minute, start_time.minute)
        self.assertEqual(Lesson.objects.get().start_time.second, start_time.second)
        self.assertEqual(Lesson.objects.get().end_time.hour, end_time.hour)
        self.assertEqual(Lesson.objects.get().end_time.minute, end_time.minute)
        self.assertEqual(Lesson.objects.get().end_time.second, end_time.second)

    def test_deleted_post(self):
        lesson = Lesson.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('webapp:lesson_delete', kwargs={'pk': lesson.pk}),
            {
                'index': 1,
                'is_saturday': False,
                'start_time': '12:12:00',
                'end_time': '14:14:00',
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('webapp:lesson_delete', kwargs={'pk': lesson.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Lesson.objects.filter(pk=lesson.pk).exists())


class AuditorySeleniumViewTest(TestCase):
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
