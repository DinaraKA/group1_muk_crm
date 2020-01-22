from django.test import TestCase
from webapp.models import Grade
from selenium.webdriver import Chrome



class GradeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Grade.objects.create(value='5000')

    def test_name_label(self):
        grade = Grade.objects.get(id=1)
        field_label = grade._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'Оценка')
        field_label = grade._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_name_max_length(self):
        grade = Grade.objects.get(id=1)
        max_length = grade._meta.get_field('value').max_length
        self.assertEquals(max_length, 50)
        max_length = grade._meta.get_field('description').max_length
        self.assertEquals(max_length, 1000)

    def test_string_representation(self):
        grade = Grade(value="5000")
        self.assertEqual(str(grade), grade.value)

    def test_object_name_is_name(self):
        grade = Grade.objects.get(id=1)
        expected_object_name = '%s' % grade.value
        self.assertEquals(expected_object_name, str(grade))


class GradeViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_grade(self):
        self.driver.get('http://localhost:8000/grades/')
        assert self.driver.current_url == 'http://localhost:8000/grades/'

    def test_created_grade(self):
        self.driver.get('http://localhost:8000/grades/add/')
        self.driver.find_element_by_name('value').send_keys('30000')
        self.driver.find_element_by_name('description').send_keys('New grade 3000')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/grades/'

    def test_updated_grade(self):
        self.driver.get('http://127.0.0.1:8000/grades/')
        self.driver.find_element_by_id('update').click()
        self.driver.find_element_by_name('value').clear()
        self.driver.find_element_by_name('value').send_keys('10')
        self.driver.find_element_by_name('description').clear()
        self.driver.find_element_by_name('description').send_keys('New grade 10 update')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/grades/'

    def test_deleted_grade(self):
        self.driver.get('http://127.0.0.1:8000/grades/')
        self.driver.find_element_by_id('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/grades/'
