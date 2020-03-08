from django.test import TestCase

from webapp.models import Announcements
from selenium.webdriver import Chrome


class AnnouncementModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Announcements.objects.create(title='TestModel')

    def test_name_label(self):
        announcement = Announcements.objects.get(id=1)
        field_label = announcement._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Заголовок')
        field_label = announcement._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст')
        field_label = announcement._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')
        field_label = announcement._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'Фото')

    def test_name_max_length(self):
        announcement = Announcements.objects.get(id=1)
        max_length = announcement._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
        max_length = announcement._meta.get_field('text').max_length
        self.assertEquals(max_length, 3000)

    def test_data_auto_now_add(self):
        announcement = Announcements.objects.get(id=1)
        auto_now_add = announcement._meta.get_field('created_at').auto_now_add
        self.assertEquals(auto_now_add, True)

    def test_upload_to(self):
        announcement = Announcements.objects.get(id=1)
        upload_to = announcement._meta.get_field('photo').upload_to
        self.assertEquals(upload_to, 'announce_image')

    def test_string_representation(self):
        announcement = Announcements(title="Test Name")
        self.assertEqual(str(announcement), announcement.title)

    def test_object_is_object(self):
        announcement = Announcements.objects.get(id=1)
        self.assertEquals(announcement.title, str(announcement.title))


class AnnouncementsSeleniumViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_announcement(self):
        self.driver.get('http://localhost:8000/announcements/')
        assert self.driver.current_url == 'http://localhost:8000/announcements/'

    def test_created_announcement(self):
        self.driver.get('http://localhost:8000/announcements/add/')
        self.driver.find_element_by_name('title').send_keys('CreateTest')
        self.driver.find_element_by_name('text').send_keys('CreateTest')
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/karamoldoevee/Downloads/test.png')
        try:
            self.driver.find_element_by_class_name('btn.btn-primary').click()
            assert self.driver.current_url == 'http://localhost:8000/announcements/'
        except:
            self.driver.find_element_by_tag_name('h3')
            assert self.driver.current_url == 'http://localhost:8000/announcements/add/'

    def test_updated_announcement(self):
        self.driver.get('http://127.0.0.1:8000/announcements/4/')
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_name('title').clear()
        self.driver.find_element_by_name('title').send_keys('UpdateTest')
        self.driver.find_element_by_name('text').clear()
        self.driver.find_element_by_name('text').send_keys('UpdateTest')
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/karamoldoevee/Downloads/test.png')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/announcements/'

    def test_deleted_announcement(self):
        self.driver.get('http://127.0.0.1:8000/announcements/4/')
        self.driver.find_element_by_class_name('btn-danger').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/announcements/'
