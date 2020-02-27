from django.test import TestCase
from django.urls import reverse, reverse_lazy

from accounts.forms import AdminPositionForm
from accounts.models import AdminPosition
from selenium.webdriver import Chrome


class AdminPositionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AdminPosition.objects.create(name='TestModel')

    def test_object_is_object(self):
        position = AdminPosition.objects.get(id=1)
        self.assertEquals(position.name, 'TestModel')

    def test_verbose_name(self):
        position = AdminPosition.objects.get(id=1)
        field_label = position._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Должность')

    def test_verbose_name_plural(self):
        self.assertEqual(str(AdminPosition._meta.verbose_name_plural), "Должности")

    def test_max_length(self):
        position = AdminPosition.objects.get(id=1)
        max_length = position._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        position = AdminPosition.objects.get(id=1)
        self.assertEqual(str(position.name), position.name)


class AdminPositionFormTest(TestCase):

    def test_renew_form_name_field_label(self):
        form = AdminPositionForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_form_valid(self):
        form_data = {'name': 'FormTest'}
        form = AdminPositionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_no_data(self):
        form = AdminPositionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class AdminPositionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AdminPosition.objects.create(
            name='Test',
        )

    def test_created_position(self):
        response = self.client.post(reverse('accounts:add_admin_position'), {'name': 'Test'})
        self.assertEqual(AdminPosition.objects.get(pk=2).name, 'Test')
        self.assertEqual(response.status_code, 302)

    def test_updated_position(self):
        position = AdminPosition.objects.get(id=1)

        response = self.client.post(
            reverse('accounts:change_admin_position', kwargs={'pk': position.id}),
            {'name': 'New Test'})

        self.assertEqual(response.status_code, 302)

        self.assertEqual(AdminPosition.objects.get().name, 'New Test')

    def test_deleted_position(self):
        position = AdminPosition.objects.get(id=1)

        self.assertEqual(AdminPosition.objects.get().name, 'Test')

        response = self.client.delete(
            reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
            {'name': 'Test'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
                                   {'name': 'Test'})

        self.assertEqual(response.status_code, 404)

        self.assertFalse(AdminPosition.objects.filter(pk=position.id).exists())


class AdminPositionSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_position(self):
        self.driver.get('http://localhost:8000/accounts/adminpositions/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/adminpositions/'

    def test_created_position(self):
        self.driver.get('http://localhost:8000/accounts/adminposition/add/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/adminpositions/'

    def test_updated_position(self):
        self.driver.get('http://127.0.0.1:8000/accounts/adminpositions/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('NewTest')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/adminpositions/'

    def test_deleted_position(self):
        self.driver.get('http://127.0.0.1:8000/accounts/adminpositions/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/adminpositions/'
