from django.test import TestCase
from django.urls import reverse, reverse_lazy

from accounts.models import SocialStatus
from selenium.webdriver import Chrome


class SocialStatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        SocialStatus.objects.create(name='Инвалид')

    def test_name_label(self):
        social_status = SocialStatus.objects.get(id=1)
        field_label = social_status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Социальный статус')

    def test_name_max_length(self):
        social_status = SocialStatus.objects.get(id=1)
        max_length = social_status._meta.get_field('name').max_length
        self.assertEquals(max_length, 30)

    def test_object_name_is_name(self):
        social_status = SocialStatus.objects.get(id=1)
        expected_object_name = '%s' % social_status.name
        self.assertEquals(expected_object_name, str(social_status))


class SocialStatusViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        SocialStatus.objects.create(
            name='Test',
        )

    def test_social_list(self):
        response = self.client.get(reverse('accounts:all_social_statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_created_social(self):
        response = self.client.post(reverse('accounts:add_social_status'), {
            'name': 'Test'
        })
        self.assertEqual(SocialStatus.objects.get(pk=2).name, 'Test')
        self.assertEqual(response.status_code, 302)

    def test_updated_social(self):
        social = SocialStatus.objects.get(id=1)
        response = self.client.post(
            reverse('accounts:change_social_status', kwargs={'pk': social.pk}),
            {
                'name': 'NewTest'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SocialStatus.objects.get().name, 'NewTest')

    def test_deleted_role(self):
        social = SocialStatus.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('accounts:delete_social_status', kwargs={'pk': social.pk}),
            {
                'name': 'NewTestModel'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('accounts:delete_social_status', kwargs={'pk': social.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(SocialStatus.objects.filter(pk=social.pk).exists())


class SocialStatusSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_social_status(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'

    def test_created_grade(self):
        self.driver.get('http://localhost:8000/accounts/social_statuses/add/')
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/accounts/social_statuses/'

    def test_updated_grade(self):
        self.driver.get('http://127.0.0.1:8000/accounts/social_statuses/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('New Test')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/social_statuses/'

    def test_deleted_grade(self):
        self.driver.get('http://127.0.0.1:8000/accounts/social_statuses/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/accounts/social_statuses/'
