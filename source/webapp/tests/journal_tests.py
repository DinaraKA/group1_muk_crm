from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from selenium.webdriver import Chrome
from webapp.models import Journal, Discipline, Grade, Theme
from webapp.views import JournalIndexView, GroupJournalCreateView


class JournalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev', username='karamoldoevee', password='aw12345678')
        Discipline.objects.create(name='Право')
        Theme.objects.create(name='Test')
        Grade.objects.create(value=5, description='Test')
        Journal.objects.create(discipline_id=1, date='2020-01-20', student_id=1, theme_id=1, grade_id=1)

    def test_student_first_name_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.first_name, 'Emir')

    def test_student_last_name_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.last_name, 'Karamoldoev')

    def test_student_username_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.username, 'karamoldoevee')

    def test_student_password_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.password, 'aw12345678')

    def test_discipline_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.discipline.name, 'Право')

    def test_theme_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.theme.name, 'Test')

    def test_grade_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.grade.value, '5')
        self.assertEquals(journal.grade.description, 'Test')

    def test_date_field(self):
        journal = Journal.objects.get(id=1)
        date = datetime(2020, 1, 20)
        self.assertEquals(journal.date.year, date.year)
        self.assertEquals(journal.date.month, date.month)
        self.assertEquals(journal.date.day, date.day)

    def test_discipine_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('discipline').verbose_name
        self.assertEquals(discipline_field, 'Дисциплина')

    def test_date_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('date').verbose_name
        self.assertEquals(discipline_field, 'Дата')

    def test_student_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('student').verbose_name
        self.assertEquals(discipline_field, 'Студент')

    def test_theme_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('theme').verbose_name
        self.assertEquals(discipline_field, 'Тема')

    def test_grade_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('grade').verbose_name
        self.assertEquals(discipline_field, 'Оценка')


class JournalSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_journal(self):
        self.driver.get('http://localhost:8000/journal/')
        assert self.driver.current_url == 'http://localhost:8000/journal/'

    def test_created_journal(self):
        self.driver.get('http://localhost:8000/journal/')
        self.driver.find_element_by_id('add_grade').click()
        self.driver.find_element_by_name('discipline').click()
        self.driver.find_element_by_name('discipline').send_keys('Русский Язык')
        self.driver.find_element_by_name('date').send_keys('2020-06-06')
        self.driver.find_element_by_name('theme').click()
        self.driver.find_element_by_name('theme').send_keys('Test')
        self.driver.find_element_by_name('grade').click()
        self.driver.find_element_by_name('grade').send_keys('5')
        self.driver.find_element_by_class_name('btn-primary').click()
        print(self.driver.current_url)
        assert self.driver.current_url == 'http://localhost:8000/journal/'

    def test_updated_journal(self):
        self.driver.get('http://127.0.0.1:8000/journal/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('discipline').click()
        self.driver.find_element_by_name('discipline').send_keys('Право')
        self.driver.find_element_by_name('date').send_keys('2020-05-05')
        self.driver.find_element_by_name('theme').click()
        self.driver.find_element_by_name('theme').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/journal/'

    def test_deleted_journal(self):
        self.driver.get('http://127.0.0.1:8000/journal/delete/1/')
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/journal/'


class JournalUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev', username='karamoldoevee', password='aw12345678')
        Discipline.objects.create(name='Право')
        Theme.objects.create(name='Test')
        Grade.objects.create(value=5, description='Test')
        Journal.objects.create(discipline_id=1, date='2020-01-20', student_id=1, theme_id=1, grade_id=1)

    def test_list_url_is_resolved(self):
        url = reverse('webapp:journal')
        self.assertEquals(resolve(url).func.view_class, JournalIndexView)

    def test_create_url_is_resolved(self):
        url = reverse('webapp:add_journal')
        self.assertEquals(resolve(url).func.view_class, GroupJournalCreateView)
