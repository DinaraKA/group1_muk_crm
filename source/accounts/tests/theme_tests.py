from django.test import TestCase
from accounts.forms import ThemeForm
from accounts.models import Theme
from selenium.webdriver import Chrome



class ThemeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Theme.objects.create(name='TestModel')

    def test_name_label(self):
        theme = Theme.objects.get(id=1)
        field_label = theme._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Админпоз')

    def test_name_max_length(self):
        theme = Theme.objects.get(id=1)
        max_length = theme._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_string_representation(self):
        theme = Theme(name="Test Name")
        self.assertEqual(str(theme), theme.name)

    def test_object_name_is_name(self):
        theme = Theme.objects.get(id=1)
        expected_object_name = '%s' % theme.name
        self.assertEquals(expected_object_name, str(theme))

    def test_verbose_name(self):
        self.assertEqual(str(Theme._meta.verbose_name), "Theme")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Theme._meta.verbose_name_plural), "Themes")


class ThemeFormTest(TestCase):

    def test_renew_form_name_field_label(self):
        form = ThemeForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_form_valid(self):
        position = Theme.objects.create(name='Test')
        form_data = {'name': 'Test'}
        form = ThemeForm(data=form_data)
        self.assertFalse(form.is_valid())


class ThemeViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_theme(self):
        self.driver.get('http://localhost:8000/accounts/themes/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/themes/'

    def test_created_theme(self):
        self.driver.get('http://localhost:8000/accounts/add_theme/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/themes/'

    def test_updated_theme(self):
        self.driver.get('http://127.0.0.1:8000/accounts/themes/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/themes/'

    def test_deleted_theme(self):
        self.driver.get('http://127.0.0.1:8000/accounts/themes/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/themes/'
