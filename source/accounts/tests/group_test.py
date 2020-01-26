from django.test import TestCase
from accounts.forms import GroupForm
from accounts.models import Group
from selenium.webdriver import Chrome



class GroupModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='TestModel')

    def test_name_label(self):
        group = Group.objects.get(id=1)
        field_label = group._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Группа')

    def test_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        group = Group(name="Test Name")
        self.assertEqual(str(group), group.name)

    def test_object_name_is_name(self):
        group = Group.objects.get(id=1)
        expected_object_name = '%s' % group.name
        self.assertEquals(expected_object_name, str(group))


class GroupFormTest(TestCase):

    def test_renew_form_name_field_label(self):
        form = GroupForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_form_valid(self):
        group = GroupForm.objects.create(name='Test')
        form_data = {'name': 'Test'}
        form = GroupForm(data=form_data)
        self.assertFalse(form.is_valid())


class GroupViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_group(self):
        self.driver.get('http://localhost:8000/accounts/groups/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'

    def test_created_group(self):
        self.driver.get('http://localhost:8000/accounts/add_group/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/groups/'

    def test_updated_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'

    def test_deleted_group(self):
        self.driver.get('http://127.0.0.1:8000/accounts/groups/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/groups/'
