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


class AnnouncementViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_announcement(self):
        self.driver.get('http://134.122.82.126/announcements/')
        assert self.driver.current_url == 'http://localhost:8000/announcements/'

    def test_detail_announcement(self):
        self.driver.get('http://134.122.82.126/announcements/')
        self.driver.find_element_by_class_name('link').click()
        assert self.driver.find_element_by_class_name('title')

    def test_created_announcement(self):
        self.driver.get('http://134.122.82.126/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.get('http://134.122.82.126/announcements/')
        self.driver.find_element_by_class_name('btn-success').click()
        self.driver.find_element_by_name('title').send_keys('CreateTest')
        self.driver.find_element_by_name('text').send_keys('CreateTest')
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/karamoldoevee/Downloads/test.png')
        try:
            self.driver.find_element_by_class_name('btn-success').click()
            assert self.driver.current_url == 'http://134.122.82.126/announcements/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_updated_announcement(self):
        self.driver.get('http://134.122.82.126/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.get('http://134.122.82.126/announcements/')
        self.driver.find_element_by_class_name('link').click()
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_name('title').clear()
        self.driver.find_element_by_name('title').send_keys('UpdateTest')
        self.driver.find_element_by_name('text').clear()
        self.driver.find_element_by_name('text').send_keys('UpdateTest')
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').clear()
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/karamoldoevee/Downloads/test.png')
        try:
            self.driver.find_element_by_class_name('btn-primary').click()
            assert self.driver.current_url == 'http://134.122.82.126/announcements/'
        except:
            assert self.driver.find_element_by_tag_name('h3')

    def test_deleted_announcement(self):
        self.driver.get('http://134.122.82.126/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        self.driver.get('http://134.122.82.126announcements/')
        self.driver.find_element_by_class_name('link').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://134.122.82.126/announcements/'
