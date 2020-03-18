from django.test import TestCase
from selenium.webdriver import Chrome


class LoginTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_create_user(self):
        self.driver.get('http://localhost:8000/accounts/user/create/')
        self.driver.find_element_by_name('username').send_keys('TestCreate20')
        self.driver.find_element_by_name('password').send_keys('test')
        self.driver.find_element_by_name('password_confirm').send_keys('test')
        self.driver.find_element_by_name('first_name').send_keys('Иван')
        self.driver.find_element_by_name('last_name').send_keys('Иванов')
        self.driver.find_element_by_name('email').send_keys('student6@mail.ru')
        self.driver.find_element_by_name('citizenship').send_keys('Гаваи')
        self.driver.find_element_by_name('series').send_keys('Ф123456789')
        self.driver.find_element_by_name('issued_by').send_keys('ГК РФ')
        self.driver.find_element_by_name('issued_date').send_keys('03/19/2019')
        self.driver.find_element_by_name('address').send_keys('Hawaii')
        self.driver.find_element_by_name('inn').send_keys('Hawaii12345')
        self.driver.find_element_by_name('nationality').send_keys('Гаваец')
        self.driver.find_element_by_name('sex').click()
        self.driver.find_element_by_name('sex').send_keys('женский')
        self.driver.find_element_by_name('birth_date').send_keys('2020-06-06')
        self.driver.find_element_by_name('patronymic').send_keys('Иванович')
        self.driver.find_element_by_name('phone_number').send_keys('+996700998877')
        self.driver.find_element_by_name('address_fact').send_keys('Марсианин')
        self.driver.find_element_by_name('role').send_keys('CreateTest')
        self.driver.find_element_by_name('status').click()
        self.driver.find_element_by_name('status').send_keys('CreateTest')
        self.driver.find_element_by_name('social_status').click()
        self.driver.find_element_by_name('social_status').send_keys('CreateTest')
        self.driver.find_element_by_name('admin_position').click()
        self.driver.find_element_by_name('admin_position').send_keys('CreateTest')
        self.driver.find_element_by_class_name('btn-success').click()
        print(self.driver.current_url)
        assert self.driver.current_url == 'http://localhost:8000/'

