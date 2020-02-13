from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.datetime_safe import datetime

from accounts.forms import GroupForm
from accounts.models import Group
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
        Group.objects.create(name='TestModel', starosta_id=1, kurator_id=2, started_at='2020-06-06')

    def test_object_is_object(self):
        group = Group.objects.get(id=1)
        date = datetime(2020, 6, 6)
        self.assertEquals(group.name, 'TestModel')
        self.assertEquals(group.starosta.username, 'karamoldoevee')
        self.assertEquals(group.kurator.username, 'karamoldoevee2')
        self.assertEquals(group.started_at.year, date.year)
        self.assertEquals(group.started_at.month, date.month)
        self.assertEquals(group.started_at.day, date.day)

    def test_verbose_name(self):
        group = Group.objects.get(id=1)
        field_label = group._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Группа')
        field_label = group._meta.get_field('starosta').verbose_name
        self.assertEquals(field_label, 'Староста')
        field_label = group._meta.get_field('kurator').verbose_name
        self.assertEquals(field_label, 'Куратор')
        field_label = group._meta.get_field('started_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_string_representation(self):
        group = Group(name="Test Name")
        self.assertEqual(str(group), group.name)


class GroupFormTest(TestCase):

    def test_form_valid_data(self):
        form = GroupForm(data={
            'name': 'TestModel',
            'students': None,
            'starosta': None,
            'kurator': None,
            'started_at': '2020-06-06'
        })
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_no_data(self):
        form = GroupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)


class GroupViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev',
                            username='karamoldoevee', password='aw12345678')
        User.objects.create(first_name='Emir2', last_name='Karamoldoev2',
                            username='karamoldoevee2', password='aw12345678')
        Group.objects.create(name='Test', starosta_id=1, kurator_id=2, started_at='2020-06-06')

    def test_group_list(self):
        response = self.client.get(reverse('accounts:groups'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_created_group(self):
        response = self.client.post(reverse('accounts:add_group'), {
            'name': 'Test',
            'students': None,
            'starosta': None,
            'kurator': None,
            'started_at': '2020-06-06'
        })
        print(Group.objects.get(pk=3).starosta)
        self.assertEqual(Group.objects.get(pk=1).name, 'Test')
        self.assertEqual(response.status_code, 302)

    def test_updated_group(self):
        group = Group.objects.get(id=1)
        response = self.client.post(
            reverse('accounts:change_group', kwargs={'pk': group.pk}),
            {
                'name': 'NewTest'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.get().name, 'NewTest')

    def test_deleted_group(self):
        group = Group.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('accounts:delete_group', kwargs={'pk': group.pk}),
            {
                'name': 'Test'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('accounts:delete_group', kwargs={'pk': group.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Group.objects.filter(pk=group.pk).exists())


class GroupSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_group(self):
        self.driver.get('http://localhost:8000/accounts/groups/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'

    def test_created_group(self):
        self.driver.get('http://localhost:8000/accounts/group/add/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_name('students').send_keys('student-1', 'student-2')
        self.driver.find_element_by_name('starosta').click()
        self.driver.find_element_by_name('starosta').send_keys('student-1')
        self.driver.find_element_by_name('kurator').click()
        self.driver.find_element_by_name('kurator').send_keys('student-2')
        self.driver.find_element_by_name('started_at').send_keys('2020-06-06')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'

    def test_updated_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_name('students').send_keys('student-3', 'student-4')
        self.driver.find_element_by_name('starosta').click()
        self.driver.find_element_by_name('starosta').send_keys('student-3')
        self.driver.find_element_by_name('kurator').click()
        self.driver.find_element_by_name('kurator').send_keys('student-4')
        self.driver.find_element_by_name('started_at').send_keys('2020-06-06')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'

    def test_deleted_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'
