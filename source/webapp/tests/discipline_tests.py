from django.test import TestCase
from django.urls import reverse, reverse_lazy

from webapp.models import Discipline
from selenium.webdriver import Chrome


class DisciplineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Discipline.objects.create(name='Китайский язык')

    def test_name_label(self):
        discipline = Discipline.objects.get(id=1)
        field_label = discipline._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Дисциплина')

    def test_name_max_length(self):
        discipline = Discipline.objects.get(id=1)
        max_length = discipline._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)

    def test_string_representation(self):
        discipline = Discipline(name="История древнего мира")
        self.assertEqual(str(discipline), discipline.name)

    def test_object_name_is_name(self):
        discipline = Discipline.objects.get(id=1)
        expected_object_name = '%s' % discipline.name
        self.assertEquals(expected_object_name, str(discipline))


class DisciplineViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Discipline.objects.create(
            name='Test'
        )

    def test_discipline_list(self):
        response = self.client.get(reverse('webapp:disciplines'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_created_discipline(self):
        response = self.client.post(reverse('webapp:add_auditory'), {
            'name': 'Other test',
            'places': 35,
            'description': 'New Test Description.'
        })
        self.assertEqual(Discipline.objects.get(pk=2).name, 'Other test')
        self.assertEqual(response.status_code, 302)

    def test_updated_discipline(self):
        discipline = Discipline.objects.get(id=1)
        response = self.client.post(
            reverse('webapp:change_discipline', kwargs={'pk': discipline.pk}),
            {
                'name': 'New Test',
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discipline.objects.get().name, 'New Test')

    def test_deleted_discipline(self):
        discipline = Discipline.objects.get(id=1)
        response = self.client.delete(
            reverse_lazy('webapp:delete_discipline', kwargs={'pk': discipline.pk}),
            {
                'name': 'Test'
            })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('webapp:delete_discipline', kwargs={'pk': discipline.pk}),
                                   {'name': 'Test'})
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Discipline.objects.filter(pk=discipline.pk).exists())


class DisciplineSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_discipline(self):
        self.driver.get('http://localhost:8000/disciplines/')
        assert self.driver.current_url == 'http://localhost:8000/disciplines/'

    def test_created_discipline(self):
        self.driver.get('http://localhost:8000/disciplines/add/')
        self.driver.find_element_by_name('name').send_keys('Международные отношения')
        self.driver.find_element_by_name('teacher').send_keys('student-1', 'student-2')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/disciplines/'

    def test_updated_disciplines(self):
        self.driver.get('http://127.0.0.1:8000/disciplines/')
        self.driver.find_element_by_id('update').click()
        self.driver.find_element_by_name('name').clear()
        self.driver.find_element_by_name('name').send_keys('Черчение')
        self.driver.find_element_by_name('teacher').send_keys('student-1', 'student-2')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/disciplines/'

    def test_deleted_disciplines(self):
        self.driver.get('http://127.0.0.1:8000/disciplines/')
        self.driver.find_element_by_id('delete').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/disciplines/'
