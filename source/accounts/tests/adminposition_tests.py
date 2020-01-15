from django.test import TestCase
from accounts.forms import AdminPositionForm
from accounts.models import AdminPosition
from selenium.webdriver import Chrome



class AdminPositionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AdminPosition.objects.create(name='TestModel')

    def test_name_label(self):
        position = AdminPosition.objects.get(id=1)
        field_label = position._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Админпоз')

    def test_name_max_length(self):
        position = AdminPosition.objects.get(id=1)
        max_length = position._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        position = AdminPosition(name="Test Name")
        self.assertEqual(str(position), position.name)

    def test_object_name_is_name(self):
        position = AdminPosition.objects.get(id=1)
        expected_object_name = '%s' % position.name
        self.assertEquals(expected_object_name, str(position))

    def test_verbose_name(self):
        self.assertEqual(str(AdminPosition._meta.verbose_name), "Позиция")

    def test_verbose_name_plural(self):
        self.assertEqual(str(AdminPosition._meta.verbose_name_plural), "Позиции")


class AdminPositionFormTest(TestCase):

    def test_renew_form_name_field_label(self):
        form = AdminPositionForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_form_valid(self):
        position = AdminPosition.objects.create(name='Test')
        form_data = {'name': 'Test'}
        form = AdminPositionForm(data=form_data)
        self.assertFalse(form.is_valid())


class AdminPositionViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_position(self):
        self.driver.get('http://localhost:8000/accounts/add_admin_position/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        response = self.client.get('http://127.0.0.1:8000/accounts/positions/')
        assert self.driver.find_element_by_name('name')

    def test_created_position(self):
        self.driver.get('http://localhost:8000/accounts/add_admin_position/')
        self.driver.find_element_by_name('name').send_keys('Mama')
        self.driver.find_element_by_class_name('btn.btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/'

    def test_updated_position(self):
        self.driver.get('http://127.0.0.1:8000/accounts/positions/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Islam_Cool')
        self.driver.find_element_by_class_name('btn.btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/'

    def test_deleted_position(self):
        self.driver.get('http://127.0.0.1:8000/accounts/positions/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn.btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/'


    # class LoginLogoutViewTest(TestCase):
    #     def setUp(self):
    #         test_user1 = User.objects.create_user(username='user', password='user')
    #
    #         test_user1.save()
    #
    #     def test_logged_in_uses_correct_template(self):
    #         login = self.client.login(username='user', password='user')
    #         response = self.client.get(reverse('webapp:index'))
    #
    #         self.assertEqual(str(response.context['user']), 'user')
    #
    #         self.assertEqual(response.status_code, 200)
    #
    #         self.assertTemplateUsed(response, 'list.html')
    #
    #     def test_logged_out_uses_correct_template(self):
    #         login = self.client.login(username='user', password='user')
    #         response = self.client.get(reverse('webapp:index'))
    #
    #         self.assertEqual(str(response.context['user']), 'user')
    #
    #         self.assertEqual(response.status_code, 200)
    #
    #         self.assertTemplateUsed(response, 'list.html')
    #
    #         logout = self.client.logout()
    #         response = self.client.get(reverse('webapp:index'))
    #
    #         self.assertEqual(response.status_code, 200)
    #
    #         self.assertTemplateUsed(response, 'list.html')


    # class AdminPositionViewTest(TestCase):
    # def test_created_position(self):
    # response = self.client.post(reverse('accounts:add_admin_position'), {'name': 'test'})
    # self.assertEqual(AdminPosition.objects.get().name, 'test')
    # self.assertEqual(response.status_code, 302)
    #
    # def test_updated_post(self):
    #     position = AdminPosition.objects.create(name='Test')
    #
    #     response = self.client.post(
    #         reverse('accounts:change_admin_position', kwargs={'pk': position.id}),
    #         {'name': 'New Test'})
    #
    #     self.assertEqual(response.status_code, 302)
    #
    #     self.assertEqual(AdminPosition.objects.get().name, 'New Test')
    #
    # def test_deleted_post(self):
    #     position = AdminPosition.objects.create(name='Test')
    #
    #     self.assertEqual(AdminPosition.objects.get().name, 'Test')
    #
    #     response = self.client.delete(
    #         reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
    #         {'name': 'Test'})
    #
    #     self.assertEqual(response.status_code, 302)
    #
    #     response = self.client.get(reverse_lazy('accounts:delete_admin_position', kwargs={'pk': position.id}),
    #                                {'name': 'Test'})
    #
    #     self.assertEqual(response.status_code, 404)
    #
    #     self.assertFalse(AdminPosition.objects.filter(pk=position.id).exists())
