from django.test import TestCase
from django.urls import reverse, reverse_lazy

from accounts.models import AdminPosition
from selenium.webdriver import Chrome


class LoginTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_log_in_as_admin(self):
        self.driver.get('http://localhost:8000/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button').click()
        assert self.driver.current_url == 'http://localhost:8000/'


class LogoutTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_logout_as_admin(self):
        self.driver.get('http://localhost:8000/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button').click()
        self.driver.get('http://localhost:8000/accounts/logout/')
        assert self.driver.current_url == 'http://localhost:8000/'


class AdminPositionModelTest(TestCase):

    def test_string_representation(self):
        entry = AdminPosition(name="Test Name")
        self.assertEqual(str(entry), entry.name)

    def test_verbose_name(self):
        self.assertEqual(str(AdminPosition._meta.verbose_name), "Позиция")

    def test_verbose_name_plural(self):
        self.assertEqual(str(AdminPosition._meta.verbose_name_plural), "Позиции")


class AdminPositionViewTest(TestCase):

    def test_created_position(self):
        response = self.client.post(reverse('accounts:add_admin_position'), {'name': 'test'})
        self.assertEqual(AdminPosition.objects.get().name, 'test')
        self.assertEqual(response.status_code, 302)

    def test_updated_post(self):
        position = AdminPosition.objects.create(name='Test')

        response = self.client.post(
            reverse('accounts:change_admin_position', kwargs={'pk': position.id}),
            {'name': 'New Test'})

        self.assertEqual(response.status_code, 302)

        self.assertEqual(AdminPosition.objects.get().name, 'New Test')

    def test_deleted_post(self):
        position = AdminPosition.objects.create(name='Test')

        self.assertEqual(AdminPosition.objects.get().name, 'Test')

        response = self.client.delete(
            reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
            {'name': 'Test'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
                                   {'name': 'Test'})

        self.assertEqual(response.status_code, 404)

        self.assertFalse(AdminPosition.objects.filter(pk=position.id).exists())