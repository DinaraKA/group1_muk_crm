from django.test import TestCase
from django.urls import reverse, reverse_lazy

from accounts.models import Role
from selenium.webdriver import Chrome


class RoleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Role.objects.create(name='TestModel')

    def test_verbose_name(self):
        role = Role.objects.get(id=1)
        field_label = role._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Роль')

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

    @classmethod
    def setUpTestData(cls):
        Role.objects.create(
            name='TestModel',
        )

    def test_role_list(self):
        response = self.client.get(reverse('accounts:roles_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestModel')

    def test_created_role(self):
        response = self.client.post(reverse('accounts:role_add'), {
            'name': 'TestModel'
        })
        self.assertEqual(Role.objects.get(pk=2).name, 'TestModel')
        self.assertEqual(response.status_code, 302)

    def test_updated_role(self):
        role = Role.objects.get(id=1)
        response = self.client.post(
            reverse('accounts:role_change', kwargs={'pk': role.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Role.objects.get().name, 'NewTestModel')

    def test_deleted_role(self):
        role = Role.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('accounts:role_delete', kwargs={'pk': role.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('accounts:role_delete', kwargs={'pk': role.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Role.objects.filter(pk=role.pk).exists())


class RoleSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_roles(self):
        self.driver.get('http://127.0.0.1:8000/accounts/roles/')
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/roles/'

    def test_created_role(self):
        self.driver.get('http://localhost:8000/accounts/roles/')
        self.driver.find_element_by_class_name('btn-outline-primary').click()
        self.driver.find_element_by_name('name').send_keys('Преподаватель')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/roles/'

    def test_updated_role(self):
        self.driver.get('http://127.0.0.1:8000/accounts/roles/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Сторож')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/roles/'

    def test_deleted_role(self):
        self.driver.get('http://127.0.0.1:8000/accounts/roles/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/roles/'
