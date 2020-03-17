from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from webapp.models import Journal, Discipline, Grade, Theme


class JournalModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Emir', last_name='Karamoldoev', username='karamoldoevee', password='aw12345678')
        Discipline.objects.create(name='Право')
        Theme.objects.create(name='Test')
        Grade.objects.create(value=5, description='Test')
        Journal.objects.create(discipline_id=1, date='2020-01-20', student_id=1, theme_id=1, grade_id=1)

    def test_student_first_name_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.first_name, 'Emir')

    def test_student_last_name_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.last_name, 'Karamoldoev')

    def test_student_username_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.username, 'karamoldoevee')

    def test_student_password_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.student.password, 'aw12345678')

    def test_discipline_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.discipline.name, 'Право')

    def test_theme_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.theme.name, 'Test')

    def test_grade_field(self):
        journal = Journal.objects.get(id=1)
        self.assertEquals(journal.grade.value, '5')
        self.assertEquals(journal.grade.description, 'Test')

    def test_date_field(self):
        journal = Journal.objects.get(id=1)
        date = datetime(2020, 1, 20)
        self.assertEquals(journal.date.year, date.year)
        self.assertEquals(journal.date.month, date.month)
        self.assertEquals(journal.date.day, date.day)

    def test_discipine_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('discipline').verbose_name
        self.assertEquals(discipline_field, 'Дисциплина')

    def test_date_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('date').verbose_name
        self.assertEquals(discipline_field, 'Дата')

    def test_student_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('student').verbose_name
        self.assertEquals(discipline_field, 'Студент')

    def test_theme_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('theme').verbose_name
        self.assertEquals(discipline_field, 'Тема')

    def test_grade_verbose_name(self):
        journal = Journal.objects.get(id=1)
        discipline_field = journal._meta.get_field('grade').verbose_name
        self.assertEquals(discipline_field, 'Оценка')
