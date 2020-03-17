from selenium.webdriver import Chrome

from django.test import TestCase

from webapp.models import Auditory


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
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_auditory(self):
        self.driver.get('http://localhost:8000/auditories/')
        assert self.driver.current_url == 'http://localhost:8000/auditories/'

o    def test_created_auditory(self):
        self.driver.get('http://localhost:8000/auditories/')
        self.driver.find_element_by_class_name('btn-success').click()
        self.driver.find_element_by_name('name').send_keys('CreateTest')
        self.driver.find_element_by_name('places').send_keys(35)
        self.driver.find_element_by_name('description').send_keys('CreateTest')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://localhost:8000/auditories/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_auditory(self):
        self.driver.get('http://127.0.0.1:8000/auditories/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('places').clear()
        self.driver.find_element_by_name('description').clear()
        self.driver.find_element_by_name('name').send_keys('Update test')
        self.driver.find_element_by_name('places').send_keys(35)
        self.driver.find_element_by_name('description').send_keys('Update test description')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://127.0.0.1:8000/auditories/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_auditory(self):
        self.driver.get('http://127.0.0.1:8000/auditories/')
        self.driver.find_element_by_class_name('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://localhost:8000/auditories/'
