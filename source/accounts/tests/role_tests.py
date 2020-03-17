from django.test import TestCase

from accounts.models import Role
from selenium.webdriver import Chrome


class RoleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Role.objects.create(name='TestModel')

    def test_verbose_name(self):
        role = Role.objects.get(id=1)
        field_label = role._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_max_length(self):
        role = Role.objects.get(id=1)
        max_length = role._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        role = Role.objects.get(id=1)
        self.assertEqual(str(role), role.name)

    def test_object_is_object(self):
        role = Role.objects.get(id=1)
        self.assertEquals(role.name, 'TestModel')


class RoleViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_roles(self):
        self.driver.get('http://localhost:8000/accounts/roles/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/roles/'

    def test_created_role(self):
        self.driver.get('http://localhost:8000/accounts/roles/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('btn-success').click()
        self.driver.find_element_by_name('name').send_keys('CreateTest')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/roles/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_role(self):
        self.driver.get('http://localhost:8000/accounts/roles/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('UpdateTest')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/roles/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_role(self):
        self.driver.get('http://localhost:8000/accounts/roles/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/roles/'
