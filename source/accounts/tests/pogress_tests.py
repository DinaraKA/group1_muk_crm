from django.test import TestCase
from selenium.webdriver import Chrome


class GroupViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_group(self):
        self.driver.get('http://localhost:8000/accounts/progress/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/progress/'

    def test_created_group(self):
        self.driver.get('http://localhost:8000/accounts/add_progress/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/progress/'

    def test_updated_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/progress/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/progress/'

    def test_deleted_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/progress/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/progress/'
