

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datetime_safe import datetime

from accounts.models import Passport


class AdminPositionModelTest(TestCase):

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

    def test_user_first_name_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.user.first_name, 'Emir')

    def test_user_last_name_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.user.last_name, 'Karamoldoev')

    def test_user_username_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.user.username, 'karamoldoevee')

    def test_user_password_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.user.password, 'aw12345678')

    def test_citizenship_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.citizenship, 'Кыргызстан')

    def test_series_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.series, 'AN4580988')

    def test_issued_by_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.issued_by, 'MKK50-55')

    def test_issued_date_field(self):
        passport = Passport.objects.get(id=1)
        date = datetime(2020, 6, 6)
        self.assertEquals(passport.issued_date.year, date.year)
        self.assertEquals(passport.issued_date.month, date.month)
        self.assertEquals(passport.issued_date.day, date.day)

    def test_address_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.address, '12-56-32')

    def test_inn_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.inn, '123456789')

    def test_nationality_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.nationality, 'Космополит')

    def test_sex_field(self):
        passport = Passport.objects.get(id=1)
        self.assertEquals(passport.sex, 'М')

    def test_birth_date_field(self):
        passport = Passport.objects.get(id=1)
        date = datetime(2020, 6, 6)
        self.assertEquals(passport.issued_date.year, date.year)
        self.assertEquals(passport.issued_date.month, date.month)
        self.assertEquals(passport.issued_date.day, date.day)

    def test_user_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_citizenship_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('citizenship').verbose_name
        self.assertEquals(field_label, 'Гражданство')

    def test_series_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('series').verbose_name
        self.assertEquals(field_label, 'Серия')

    def test_issued_by_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').verbose_name
        self.assertEquals(field_label, 'Кем выдан')

    def test_issued_date_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_date').verbose_name
        self.assertEquals(field_label, 'Дата выдачи')

    def test_address_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'Адрес')

    def test_inn_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('inn').verbose_name
        self.assertEquals(field_label, 'ИНН')

    def test_nationality_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('nationality').verbose_name
        self.assertEquals(field_label, 'Национальность')

    def test_sex_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('sex').verbose_name
        self.assertEquals(field_label, 'Пол')

    def test_birth_date_verbose_name(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('birth_date').verbose_name
        self.assertEquals(field_label, 'Дата Рождения')

    def test_citizenship_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('citizenship').max_length
        self.assertEquals(field_label, 50)

    def test_series_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('series').max_length
        self.assertEquals(field_label, 15)

    def test_issued_bymax_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').max_length
        self.assertEquals(field_label, 255)

    def test_address_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('address').max_length
        self.assertEquals(field_label, 100)

    def test_inn_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('inn').max_length
        self.assertEquals(field_label, 50)

    def test_nationality_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('nationality').max_length
        self.assertEquals(field_label, 30)

    def test_sex_max_length(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('sex').max_length
        self.assertEquals(field_label, 15)

    def test_citizenship_default(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('citizenship').default
        self.assertEquals(field_label, 'Кыргызская Республика')

    def test_issued_by_blank(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').blank
        self.assertEquals(field_label, 'True')

    def test_inn_blank(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('inn').blank
        self.assertEquals(field_label, 'True')

    def test_nationality_blank(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('nationality').blank
        self.assertEquals(field_label, 'True')

    def test_issued_by_null(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('issued_by').null
        self.assertEquals(field_label, 'True')

    def test_inn_null(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('inn').null
        self.assertEquals(field_label, 'True')

    def test_nationality_null(self):
        passport = Passport.objects.get(id=1)
        field_label = passport._meta.get_field('nationality').null
        self.assertEquals(field_label, 'True')