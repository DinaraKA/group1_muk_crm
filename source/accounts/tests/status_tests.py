from django.test import TestCase
from django.urls import reverse, reverse_lazy

from accounts.models import Status
from selenium.webdriver import Chrome


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='TestModel')

    def test_verbose_name(self):
        status = Status.objects.get(id=1)
        field_label = status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Статус')

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

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(
            name='TestModel',
        )

    def test_status_list(self):
        response = self.client.get(reverse('accounts:statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestModel')

    def test_created_status(self):
        response = self.client.post(reverse('accounts:add_status'), {
            'name': 'TestModel'
        })
        self.assertEqual(Status.objects.get(pk=1).name, 'TestModel')
        self.assertEqual(response.status_code, 302)

    def test_updated_status(self):
        status = Status.objects.get(id=1)
        response = self.client.post(
            reverse('accounts:change_status', kwargs={'pk': status.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.get().name, 'NewTestModel')

    def test_deleted_status(self):
        status = Status.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('accounts:delete_status', kwargs={'pk': status.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('accounts:delete_status', kwargs={'pk': status.pk}),
                                   {'name': 'TestModel'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Status.objects.filter(pk=status.pk).exists())


class StatusSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_roles(self):
        self.driver.get('http://127.0.0.1:8000/accounts/statuses/')
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/statuses/'

    def test_created_status(self):
        self.driver.get('http://localhost:8000/accounts/statuses/')
        self.driver.find_element_by_class_name('btn-outline-primary').click()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/statuses/'

    def test_updated_status(self):
        self.driver.get('http://127.0.0.1:8000/accounts/statuses/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/statuses/'

    def test_deleted_status(self):
        self.driver.get('http://127.0.0.1:8000/accounts/statuses/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/statuses/'
