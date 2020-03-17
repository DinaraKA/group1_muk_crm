from django.test import TestCase

from accounts.models import Status
from selenium.webdriver import Chrome


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='TestModel')

    def test_verbose_name(self):
        status = Status.objects.get(id=1)
        field_label = status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_max_length(self):
        status = Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        status = Status.objects.get(id=1)
        self.assertEqual(str(status), status.name)

    def test_object_is_object(self):
        status = Status.objects.get(id=1)
        self.assertEquals(status.name, 'TestModel')


class StatusViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_roles(self):
        self.driver.get('http://localhost:8000/accounts/statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/statuses/'

    def test_created_status(self):
        self.driver.get('http://localhost:8000/accounts/statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('btn-success').click()
        self.driver.find_element_by_name('name').send_keys('CreateTest')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/statuses/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_status(self):
        self.driver.get('http://localhost:8000/accounts/statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('UpdateTest')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/statuses/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_status(self):
        self.driver.get('http://localhost:8000/accounts/statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/statuses/'
