from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datetime_safe import datetime

from accounts.models import Passport


class PassportModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev',
                            username='karamoldoevee', password='aw12345678')
        Passport.objects.create(
            user_id=1,
            citizenship='Кыргызстан',
            series='AN4580988',
            issued_by='MKK50-55',
            issued_date='2020-06-06',
            address='12-56-32',
            inn='123456789',
            nationality='Космополит',
            sex='М',
            birth_date='2020-06-06'
        )

    def test_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.user.first_name, 'Emir')
        self.assertEquals(passport.user.last_name, 'Karamoldoev')
        self.assertEquals(passport.user.username, 'karamoldoevee')
        self.assertEquals(passport.user.password, 'aw12345678')
        self.assertEquals(passport.citizenship, 'Кыргызстан')
        self.assertEquals(passport.series, 'AN4580988')
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.issued_by, 'MKK50-55')
        date = datetime(2020, 6, 6)
        self.assertEquals(passport.issued_date.year, date.year)
        self.assertEquals(passport.issued_date.month, date.month)
        self.assertEquals(passport.issued_date.day, date.day)
        self.assertEquals(passport.address, '12-56-32')
        self.assertEquals(passport.inn, '123456789')
        self.assertEquals(passport.nationality, 'Космополит')
        self.assertEquals(passport.sex, 'М')
        date = datetime(2020, 6, 6)
        self.assertEquals(passport.issued_date.year, date.year)
        self.assertEquals(passport.issued_date.month, date.month)
        self.assertEquals(passport.issued_date.day, date.day)

    def test_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')
        field_label = passport._meta.get_field('citizenship').verbose_name
        self.assertEquals(field_label, 'Гражданство')
        field_label = passport._meta.get_field('series').verbose_name
        self.assertEquals(field_label, 'Серия')
        field_label = passport._meta.get_field('issued_by').verbose_name
        self.assertEquals(field_label, 'Кем выдан')
        field_label = passport._meta.get_field('issued_date').verbose_name
        self.assertEquals(field_label, 'Дата выдачи')
        field_label = passport._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'Адрес')
        field_label = passport._meta.get_field('inn').verbose_name
        self.assertEquals(field_label, 'ИНН')
        field_label = passport._meta.get_field('nationality').verbose_name
        self.assertEquals(field_label, 'Национальность')
        field_label = passport._meta.get_field('sex').verbose_name
        self.assertEquals(field_label, 'Пол')
        field_label = passport._meta.get_field('birth_date').verbose_name
        self.assertEquals(field_label, 'Дата Рождения')

    def test_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('citizenship').max_length
        self.assertEquals(field_label, 50)
        field_label = passport._meta.get_field('series').max_length
        self.assertEquals(field_label, 15)
        field_label = passport._meta.get_field('issued_by').max_length
        self.assertEquals(field_label, 255)
        field_label = passport._meta.get_field('address').max_length
        self.assertEquals(field_label, 100)
        field_label = passport._meta.get_field('inn').max_length
        self.assertEquals(field_label, 50)
        field_label = passport._meta.get_field('nationality').max_length
        self.assertEquals(field_label, 30)
        field_label = passport._meta.get_field('sex').max_length
        self.assertEquals(field_label, 15)

    def test_default(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('citizenship').default
        self.assertEquals(field_label, 'Кыргызская Республика')

    def test_blank(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').blank
        self.assertEquals(field_label, 'True')
        field_label = passport._meta.get_field('inn').blank
        self.assertEquals(field_label, 'True')
        field_label = passport._meta.get_field('nationality').blank
        self.assertEquals(field_label, 'True')

    def test_null(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').null
        self.assertEquals(field_label, 'True')
        field_label = passport._meta.get_field('inn').null
        self.assertEquals(field_label, 'True')
        field_label = passport._meta.get_field('nationality').null
        self.assertEquals(field_label, 'True')