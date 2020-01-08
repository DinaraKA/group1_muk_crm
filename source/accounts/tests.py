from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginLogoutViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='user', password='user')

        test_user1.save()

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user', password='user')
        response = self.client.get(reverse('webapp:index'))

        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'index.html')

    def test_logged_out_uses_correct_template(self):
        login = self.client.login(username='user', password='user')
        response = self.client.get(reverse('webapp:index'))

        self.assertEqual(str(response.context['user']), 'user')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'index.html')

        logout = self.client.logout()
        response = self.client.get(reverse('webapp:index'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'index.html')