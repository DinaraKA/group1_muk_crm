from urllib import response
from django.test import TestCase
from django.urls import reverse

from webapp.models import News
from selenium.webdriver import Chrome


class NewsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='TestModel')

    def test_name_label(self):
        news = News.objects.get(id=1)
        field_label = news._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Заголовок')
        field_label = news._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст')
        field_label = news._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')
        field_label = news._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'Фото')

    def test_name_max_length(self):
        news = News.objects.get(id=1)
        max_length = news._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
        max_length = news._meta.get_field('text').max_length
        self.assertEquals(max_length, 3000)

    def test_data_auto_now_add(self):
        news = News.objects.get(id=1)
        auto_now_add = news._meta.get_field('created_at').auto_now_add
        self.assertEquals(auto_now_add, True)

    def test_upload_to(self):
        news = News.objects.get(id=1)
        upload_to = news._meta.get_field('photo').upload_to
        self.assertEquals(upload_to, 'news_images')

    def test_string_representation(self):
        news = News(title="Test Name")
        self.assertEqual(str(news), news.title)

    def test_object_title_is_title(self):
        news = News.objects.get(id=1)
        expected_object_name = '%s' % news.title
        self.assertEquals(expected_object_name, str(news))


class NewsListViewTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_list_news(self):
        self.driver.get('http://localhost:8000/news/')
        assert self.driver.current_url == 'http://localhost:8000/news/'

    def test_created_news(self):
        self.driver.get('http://localhost:8000/news/add/')
        self.driver.find_element_by_name('title').send_keys('Test news')
        self.driver.find_element_by_name('text').send_keys('Test news888888')
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/aisuluu/projects/group1_muk_crm/source/uploads/news_images/aidin.jpg')
        self.driver.find_element_by_class_name('btn-primary').click()
        assert self.driver.current_url == 'http://localhost:8000/news/'

    #
    # def test_news_detail(self):
    #     news = test_created_news(title='BESIIIT.', text='Ghbdtn', photo='/home/aisuluu/projects/group1_muk_crm/source/uploads/news_images/aidin.jpg')
    #     url = reverse('webapp:news_detail', args=(news.id,))
    #     response = self.driver.get(url)
    #     self.assertContains(response, news.title, news.text, news.photo)

    def test_updated_news(self):
        self.driver.get('http://127.0.0.1:8000/news/edit/')
        self.driver.find_element_by_class_name('update').click()
        self.driver.find_element_by_name('title').clear()
        self.driver.find_element_by_name('title').send_keys('News test2')
        self.driver.find_element_by_name('text').clear()
        self.driver.find_element_by_name('text').send_keys('it new news')
        self.driver.find_element_by_name('photo').clear()
        self.driver.find_element_by_xpath('//*[@id="id_photo"]').send_keys('/home/aisuluu/projects/group1_muk_crm/source/uploads/news_images/nadina.jpg')
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/news/'

    def test_deleted_news(self):
        self.driver.get('http://127.0.0.1:8000/news/delete/')
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_class_name('btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:8000/news/'
