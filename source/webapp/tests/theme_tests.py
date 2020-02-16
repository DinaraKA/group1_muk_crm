from django.test import TestCase
from django.urls import reverse, reverse_lazy

from webapp.models import Theme
from selenium.webdriver import Chrome


class ThemeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Theme.objects.create(name='TestModel')

    def test_verbose_name(self):
        theme = Theme.objects.get(id=1)
        field_label = theme._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Тема')

    def test_max_length(self):
        theme = Theme.objects.get(id=1)
        max_length = theme._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_string_representation(self):
        theme = Theme.objects.get(id=1)
        self.assertEqual(str(theme), theme.name)

    def test_object_is_object(self):
        theme = Theme.objects.get(id=1)
        self.assertEquals(theme.name, 'TestModel')


class ThemeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Theme.objects.create(
            name='TestModel',
        )

    def test_theme_list(self):
        response = self.client.get(reverse('webapp:themes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestModel')

    def test_created_theme(self):
        response = self.client.post(reverse('webapp:add_theme'), {
            'name': 'TestModel'
        })
        self.assertEqual(Theme.objects.get(pk=2).name, 'TestModel')
        self.assertEqual(response.status_code, 302)

    def test_updated_theme(self):
        theme = Theme.objects.get(id=1)
        response = self.client.post(
            reverse('webapp:change_theme', kwargs={'pk': theme.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Theme.objects.get().name, 'NewTestModel')

    def test_deleted_theme(self):
        theme = Theme.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('webapp:delete_theme', kwargs={'pk': theme.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('webapp:delete_theme', kwargs={'pk': theme.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Theme.objects.filter(pk=theme.pk).exists())


class ThemeSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_theme(self):
        self.driver.get('http://127.0.0.1:8000/themes/')
        assert self.driver.current_url == 'http://127.0.0.1:8000/themes/'

    def test_created_theme(self):
        self.driver.get('http://localhost:8000/themes/')
        self.driver.find_element_by_class_name('btn-outline-primary').click()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/themes/'

    def test_updated_theme(self):
        self.driver.get('http://127.0.0.1:8000/themes/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/themes/'

    def test_deleted_theme(self):
        self.driver.get('http://127.0.0.1:8000/themes/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/themes/'
