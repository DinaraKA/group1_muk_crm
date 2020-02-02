from django.contrib.auth.models import User
from django.test import TestCase
from selenium.webdriver import Chrome
from webapp.models import Journal, Discipline, Grade, Theme


class JournalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Discipline.objects.create(name='Право')
        User.objects.create(username='Test')
        Theme.objects.create(name='Test')
        Grade.objects.create(value=5, description='Test')
        Journal.objects.create(discipline_id=1, date='2020-01-20', student_id=1, theme_id=1, grade_id=1)

    def test_discipine_field(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('discipline').verbose_name
        self.assertEquals(discipline_field, 'Дисциплина')

    def test_date_field(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('date').verbose_name
        self.assertEquals(discipline_field, 'Дата')

    def test_student_field(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('student').verbose_name
        self.assertEquals(discipline_field, 'Студент')

    def test_theme_field(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('theme').verbose_name
        self.assertEquals(discipline_field, 'Тема')

    def test_grade_field(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('grade').verbose_name
        self.assertEquals(discipline_field, 'Оценка')

    def test_whatever_creation(self):
        w = Journal.objects.create(discipline_id=1, date='2020-01-20', student_id=1, theme_id=1, grade_id=1)
        self.assertTrue(isinstance(w, Journal))
        self.assertEqual(w, Journal)


class GroupViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_group(self):
        self.driver.get('http://localhost:8000/webapp/journal/')
        assert self.driver.current_url == 'http://localhost:8000/webapp/journal/'

    def test_created_group(self):
        self.driver.get('http://localhost:8000/accounts/add_journal/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/webapp/journal/'

    def test_updated_group(self):
        self.driver.get('http://127.0.0.1:8000/webapp/journal/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/webapp/journal/'

    def test_deleted_group(self):
        self.driver.get('http://127.0.0.1:8000/webapp/journal')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/webapp/journal/'
