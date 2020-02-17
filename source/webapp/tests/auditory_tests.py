from selenium.webdriver import Chrome

from django.test import TestCase
from django.urls import reverse, reverse_lazy, resolve

from webapp.models import Auditory
from webapp.views.auditory_views import AuditoryListView, AuditoryCreateView, AuditoryUpdateView, AuditoryDeleteView


class AuditoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Auditory.objects.create(
            name='Test',
            places=33,
            description='Test Description.'
        )

    def test_field(self):
        auditory = Auditory.objects.get(id=1)
        self.assertEquals(auditory.name, 'Test')
        auditory = Auditory.objects.get(id=1)
        self.assertEquals(auditory.places, 33)
        self.assertEquals(auditory.description, 'Test Description.')

    def test_verbose_name(self):
        auditory = Auditory.objects.get(id=1)
        field_label = auditory._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')
        field_label = auditory._meta.get_field('places').verbose_name
        self.assertEquals(field_label, 'Вместимость')
        field_label = auditory._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_length(self):
        auditory = Auditory.objects.get(id=1)
        field_label = auditory._meta.get_field('name').max_length
        self.assertEquals(field_label, 100)
        field_label = auditory._meta.get_field('description').max_length
        self.assertEquals(field_label, 2000)

    def test_blank(self):
        auditory = Auditory.objects.get(id=1)
        field_label = auditory._meta.get_field('name').blank
        self.assertEquals(field_label, False)
        field_label = auditory._meta.get_field('places').blank
        self.assertEquals(field_label, True)
        field_label = auditory._meta.get_field('description').blank
        self.assertEquals(field_label, True)

    def test_null(self):
        auditory = Auditory.objects.get(id=1)
        field_label = auditory._meta.get_field('name').null
        self.assertEquals(field_label, False)
        field_label = auditory._meta.get_field('places').null
        self.assertEquals(field_label, True)
        field_label = auditory._meta.get_field('description').null
        self.assertEquals(field_label, True)


class AuditoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Auditory.objects.create(
            name='Test',
            places=33,
            description='Test Description.'
        )

    def test_auditory_list(self):
        response = self.client.get(reverse('webapp:auditories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        self.assertContains(response, 33)
        self.assertContains(response, 'Test Description.')

    def test_created_position(self):
        response = self.client.post(reverse('webapp:add_auditory'), {
            'name': 'Other Test',
            'places': 35,
            'description': 'New Test Description.'
        })
        self.assertEqual(Auditory.objects.get(pk=2).name, 'Other Test')
        self.assertEqual(response.status_code, 302)

    def test_updated_post(self):
        auditory = Auditory.objects.get(id=1)
        response = self.client.post(
            reverse('webapp:change_auditory', kwargs={'pk': auditory.pk}),
            {
                'name': 'New Test',
                'places': 35,
                'description': 'New Test Description.'
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Auditory.objects.get().name, 'New Test')
        self.assertEqual(Auditory.objects.get().places, 35)
        self.assertEqual(Auditory.objects.get().description, 'New Test Description.')

    def test_deleted_post(self):
        auditory = Auditory.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('webapp:delete_auditory', kwargs={'pk': auditory.pk}),
            {
                'name': 'New Test',
                'places': 35,
                'description': 'New Test Description.'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('webapp:delete_auditory', kwargs={'pk': auditory.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Auditory.objects.filter(pk=auditory.pk).exists())


class AuditorySeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_auditory(self):
        self.driver.get('http://localhost:8000/accounts/adminpositions/')
        assert self.driver.current_url == 'http://localhost:8000/accounts/adminpositions/'

    def test_created_auditory(self):
        self.driver.get('http://localhost:8000/auditories/add/')
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_name('places').send_keys(35)
        self.driver.find_element_by_name('description').send_keys('Test description')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/auditories/'

    def test_updated_auditory(self):
        self.driver.get('http://127.0.0.1:8000/auditories/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('places').clear()
        self.driver.find_element_by_name('description').clear()
        self.driver.find_element_by_name('name').send_keys('Test')
        self.driver.find_element_by_name('places').send_keys(35)
        self.driver.find_element_by_name('description').send_keys('Test description')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/auditories/'

    def test_deleted_auditory(self):
        self.driver.get('http://127.0.0.1:8000/auditories/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/auditories/'


class AuditoryUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Auditory.objects.create(
            name='Test',
            places=33,
            description='Test Description.'
        )

    def test_list_url_is_resolved(self):
        url = reverse('webapp:auditories')
        self.assertEquals(resolve(url).func.view_class, AuditoryListView)

    def test_create_url_is_resolved(self):
        url = reverse('webapp:add_auditory')
        self.assertEquals(resolve(url).func.view_class, AuditoryCreateView)

    # def test_update_url_is_resolved(self):
    #     url = reverse('webapp:change_auditory')
    #     self.assertEquals(resolve(url).func.view_class, AuditoryUpdateView)
    #
    # def test_delete_url_is_resolved(self):
    #     url = reverse('webapp:delete_auditory')
    #     self.assertEquals(resolve(url).func.view_class, AuditoryDeleteView)
