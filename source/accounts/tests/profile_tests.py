from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile
from accounts.models import Status, AdminPosition, SocialStatus


class PassportModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev',
                            username='karamoldoevee', password='aw12345678')
        Status.objects.create(name='Test')
        AdminPosition.objects.create(name='Test')
        SocialStatus.objects.create(name='Test')
        profile = Profile.objects.create(
            user_id=1,
            patronymic='TestPatronymic',
            phone_number='0999999999',
            address_fact='TestAddressFact',
            status_id=1,
            admin_position_id=1,
            social_status_id=1
        )

    def test_field(self):
        profile = Profile.objects.get(id=1)
        self.assertEquals(profile.user.id, 1)
        self.assertEquals(profile.patronymic, 'TestPatronymic')
        self.assertEquals(profile.phone_number, '0999999999')
        self.assertEquals(profile.address_fact, 'TestAddressFact')
        self.assertEquals(profile.status.name, 'Test')
        self.assertEquals(profile.admin_position.name, 'Test')
        self.assertEquals(profile.social_status.name, 'Test')

    def test_verbose_name(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('patronymic').verbose_name
        self.assertEquals(field_label, 'Отчество')
        field_label = profile._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'Номер телефона')
        field_label = profile._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'Фото')
        field_label = profile._meta.get_field('address_fact').verbose_name
        self.assertEquals(field_label, 'Фактический Адрес')
        field_label = profile._meta.get_field('role').verbose_name
        self.assertEquals(field_label, 'Роль')
        field_label = profile._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Статус')
        field_label = profile._meta.get_field('admin_position').verbose_name
        self.assertEquals(field_label, 'Должность')
        field_label = profile._meta.get_field('social_status').verbose_name
        self.assertEquals(field_label, 'Соц. Статус')

    def test_max_length(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('patronymic').max_length
        self.assertEquals(field_label, 30)
        field_label = profile._meta.get_field('address_fact').max_length
        self.assertEquals(field_label, 100)

    def test_default(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('status').default
        self.assertEquals(field_label, None)

    def test_blank(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('patronymic').blank
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('phone_number').blank
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('photo').blank
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('admin_position').blank
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('social_status').blank
        self.assertEquals(field_label, True)

    def test_null(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('patronymic').null
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('phone_number').null
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('photo').null
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('admin_position').null
        self.assertEquals(field_label, True)
        field_label = profile._meta.get_field('social_status').null
        self.assertEquals(field_label, True)
