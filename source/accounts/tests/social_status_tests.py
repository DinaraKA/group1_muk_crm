from django.test import TestCase

from accounts.models import SocialStatus
from selenium.webdriver import Chrome


class SocialStatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        SocialStatus.objects.create(name='ModelTest')

    def test_name_label(self):
        social_status = SocialStatus.objects.get(id=1)
        field_label = social_status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_name_max_length(self):
        social_status = SocialStatus.objects.get(id=1)
        max_length = social_status._meta.get_field('name').max_length
        self.assertEquals(max_length, 30)

    def test_object_name_is_name(self):
        social_status = SocialStatus.objects.get(id=1)
        expected_object_name = '%s' % social_status.name
        self.assertEquals(expected_object_name, str(social_status))


class SocialStatusViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'

    def test_created_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/add/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_name('name').send_keys('CreateTest')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('UpdateTest')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'
