from django.test import TestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome


class LoginTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_log_in_as_admin(self):
        self.driver.get('http://localhost:8000/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'
        try:
            link = self.driver.find_element_by_link_text("Привет, admin!")
        except NoSuchElementException:
            link = None

    def test_login_error(self):
        self.driver.get('http://localhost:8000/accounts/login/')
        self.driver.find_element_by_name('username').send_keys('adminanet')
        self.driver.find_element_by_name('password').send_keys('adminanet')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url.split('?')[0] == 'http://localhost:8000/accounts/login/'
        error = self.driver.find_element_by_css_selector('.text-danger')
        assert error.text == "Неверное имя пользователя или пароль."
