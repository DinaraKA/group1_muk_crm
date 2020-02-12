from django.test import TestCase
from accounts.models import SocialStatus
from selenium.webdriver import Chrome


class SocialStatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        SocialStatus.objects.create(name='Инвалид')

    def test_name_label(self):
        social_status = SocialStatus.objects.get(id=1)
        field_label = social_status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Социальный статус')

    def test_name_max_length(self):
        social_status = SocialStatus.objects.get(id=1)
        max_length = social_status._meta.get_field('name').max_length
        self.assertEquals(max_length, 30)

    def test_object_name_is_name(self):
        social_status = SocialStatus.objects.get(id=1)
        expected_object_name = '%s' % social_status.name
        self.assertEquals(expected_object_name, str(social_status))


class GradeViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'

    def test_created_grade(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/add/')
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'

    def test_updated_grade(self):
        self.driver.get('http://127.0.0.1:8000/accounts/social_status/change/1/')
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('New Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/social_statuses/'

    def test_deleted_grade(self):
        self.driver.get('http://127.0.0.1:8000/accounts/social_status/delete/1/')
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/social_statuses/'
