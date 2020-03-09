from django.contrib.auth.models import User
from django.test import TestCase

from django.utils.datetime_safe import datetime
from accounts.models import StudyGroup
from selenium.webdriver import Chrome


class GroupModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev',
                            username='karamoldoevee', password='aw12345678')
        User.objects.create(first_name='Emir2', last_name='Karamoldoev2',
                            username='karamoldoevee2', password='aw12345678')
        user = User.objects.create(first_name='Emir3', last_name='Karamoldoev3',
                                   username='karamoldoevee3', password='aw12345678')
        StudyGroup.objects.create(name='TestModel', group_leader_id=1, head_teaher_id=2, started_at='2020-06-06')

    def test_object_is_object(self):
        group = \
            StudyGroup.objects.get(id=1)
        date = datetime(2020, 6, 6)
        self.assertEquals(group.name, 'TestModel')
        self.assertEquals(group.group_leader.username, 'karamoldoevee')
        self.assertEquals(group.head_teaher.username, 'karamoldoevee2')
        self.assertEquals(group.started_at.year, date.year)
        self.assertEquals(group.started_at.month, date.month)
        self.assertEquals(group.started_at.day, date.day)

    def test_verbose_name(self):
        group = StudyGroup.objects.get(id=1)
        field_label = group._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Группа')
        field_label = group._meta.get_field('group_leader').verbose_name
        self.assertEquals(field_label, 'Староста')
        field_label = group._meta.get_field('head_teaher').verbose_name
        self.assertEquals(field_label, 'Куратор')
        field_label = group._meta.get_field('started_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_max_length(self):
        group = StudyGroup.objects.get(id=1)
        max_length = group._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_string_representation(self):
        group = StudyGroup(name="Test Name")
        self.assertEqual(str(group), group.name)


class GroupViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_group(self):
        self.driver.get('http://localhost:8000/accounts/groups/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'

    def test_created_group(self):
        self.driver.get('http://localhost:8000/accounts/group/add/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_name('name').send_keys('CreateTest')
        self.driver.find_element_by_name('students').send_keys('Айдай Исаева')
        self.driver.find_element_by_name('group_leader').click()
        self.driver.find_element_by_name('group_leader').send_keys('Айдай Исаева')
        self.driver.find_element_by_name('head_teaher').click()
        self.driver.find_element_by_name('head_teaher').send_keys('Фарид Халиков')
        self.driver.find_element_by_name('started_at').send_keys('2020-06-06')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('UpdateTest')
        self.driver.find_element_by_name('students').send_keys('Айдай Исаева')
        self.driver.find_element_by_name('group_leader').click()
        self.driver.find_element_by_name('group_leader').send_keys('Марина Ложкина')
        self.driver.find_element_by_name('head_teaher').click()
        self.driver.find_element_by_name('head_teaher').send_keys('Фарид Халиков')
        self.driver.find_element_by_name('started_at').send_keys('2020-06-06')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'
